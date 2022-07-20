from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from coupon.forms import AddCouponForm
from shop.models import Item
from .forms import AddItemForm
from .cart import Cart

@require_POST
def add(request, item_id):
    cart=Cart(request) #나만의 공간
    item=get_object_or_404(Item, id=item_id)

    #클라이언트->서버로 데이터를 전달
    #유효성검사, injection 전처리
    form=AddItemForm(request.POST)
    if form.is_valid():
        cd=form.cleaned_data #injection 끝난 데이터
        cart.add(item=item, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')

def remove(request, item_id):
    cart=Cart(request)
    item=get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:detail')

def detail(request):
    cart=Cart(request)
    add_coupon=AddCouponForm()
    for item in cart:
        item['quantity_form']=AddItemForm(initial={'quantity':item['quantity'], 'is_update':True})
    return render(request, 'cart/detail.html', {'cart':cart, 'add_coupon':add_coupon})

def input_item(request):
    if request.POST:
        list_item=request.POST.getlist('item1')
    return redirect('orders:order_create', {'list_item':list_item})