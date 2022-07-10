from django.shortcuts import render, get_object_or_404
from .models import *
from cart.cart import Cart
from .forms import *

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.amount
                order.save()
            for product in cart:
                OrderItem.objects.create(order=order, item=product['item'], price=product['item_price'], quantity=product['quantity'])

            cart.clear()
            return render(request, 'order/created.html', {'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart':cart, 'form':form})



# ajax로 결제 후에 보여줄 결제 완료 화면
def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    return render(request,'order/created.html',{'order':order})
