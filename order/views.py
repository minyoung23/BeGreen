from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView

from shop.models import Category
from .models import *
from cart.cart import Cart
from .forms import *

#주문자 정보를 입력받는 페이지
def order_create(request):
    cart = Cart(request) #cart 가 있어야 계산 가능
    if request.method == 'POST':
        form = OrderCreateForm(request.POST) #입력받은 폼을 validation받으면
        if form.is_valid(): #멀쩡하면
            order = form.save()
            if cart.coupon:
                order.coupon = cart.coupon
                #order.discount = cart.coupon.amount #할인가에 맞춰서. cart/views.py에
                order.discount=cart.get_discount_total() #위의 것보다 좀더 안전한 방식
                order.save()
            for product in cart:
                OrderItem.objects.create(order=order, item=product['item'], item_price=product['item_price'], quantity=product['quantity'])
            #제품을 다 추가한 후 clear
            cart.clear()
            return render(request, 'order/created.html', {'order':order})
    else:
        form = OrderCreateForm() #주문자 정보 form에 입력받음
    #잘못된 입력정보를 받은 경우 create.html에 돌려보림
    return render(request, 'order/create.html', {'cart':cart, 'form':form})



# ajax로 결제 후에 보여줄 결제 완료 화면. 자바스크립트를 이용해서 정보 처리.
# 자바스크립트가 동작하지 않느 환경에서도 주문은 가능해야 한다.
def order_complete(request):
    categories=Category.objects.all()
    order_id = request.GET.get('order_id')
    #order = Order.objects.get(id=order_id)
    order=get_object_or_404(Order, id=order_id)
    #주문한 수량만큼 빼주기
    if order.paid is True:
        for i in range(len(order.products.all())):
            change=order.products.all()[i].item
            change.item_amt-=order.products.all()[i].quantity
            if change.item_amt <5:
                change.item_amt+=20
            change.save()

    return render(request,'order/created.html',{'order':order, 'categories':categories})


# 결제를 위한 임포트
from django.views.generic.base import View
from django.http import JsonResponse

#iamport와 ajax로 통신하기 위한 뷰
#뷰에서 이미 분기되어있음
class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False) #쿼리가 날아가지 않게
            if cart.coupon:
                order.coupon = cart.coupon
                #order.discount = cart.coupon.amount
                order.discount=cart.get_discount_total()
            order.save() #교재랑 다른 부분. 이때 쿼리를 날아가게 함
            for product in cart:
                OrderItem.objects.create(order=order, item=product['item'], item_price=product['item_price'],
                                         quantity=product['quantity'])
            cart.clear()
            #응답만들어주기
            data = {
                "order_id": order.id
            }
            return JsonResponse(data)
        else: #폼이 valid 하지 않았을 때 401
            return JsonResponse({}, status=401)

# ajax로 받은 데이터를 통해서 merchant_order_id를 생성하기 위한 뷰
#자바스크립트가 적용될 때 적용되는 뷰. 아니면 order_create 뷰
class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated: #로그인 했는가의 여부
            return JsonResponse({"authenticated":False}, status=403)

        #각 해당객체 가져오기
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except: #merchant_order_id를 가지고 결제 여부 조회
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# iamport의 transaction과 db의 trans가 일치하는지 검증하는 뷰
class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            #trans.success = True
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderList(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'order_list'


class OrderItemList(ListView):
    model = OrderItem

    template_name = 'orderitem_list.html'
    context_object_name = 'orderitem_list'
