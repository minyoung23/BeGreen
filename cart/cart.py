from django.conf import settings
from shop.models import Item
from coupon.models import Coupon

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id=self.session.get('coupon_id')


    def __len__(self):
        return sum(product['quantity'] for product in self.cart.values())

    def __iter__(self):
        item_ids = self.cart.keys()

        items = Item.objects.filter(id__in=item_ids)

        for item in items:
            self.cart[str(item.id)]['item'] = item

        for product in self.cart.values():
            int(product['item_price'])
            product['total_price'] = int(product['item_price']) * product['quantity']

            yield product


    def add(self, item, quantity=1, is_update=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity':0, 'item_price':str(item.item_price)}

        if is_update:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del(self.cart[item_id])
            self.save()

    def clear(self): #장바구니 비우기
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] = None
        self.session.modified = True


    def get_item_total(self):
        return sum(int(product['item_price'])*product['quantity'] for product in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount_total(self):
        if self.coupon:
            if self.get_item_total() >= self.coupon.amount:
                return self.coupon.amount
        return 0

    def get_total_price(self):
        return self.get_item_total() - self.get_discount_total()


