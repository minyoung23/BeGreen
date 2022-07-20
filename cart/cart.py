from django.conf import settings
from shop.models import Item
from coupon.models import Coupon

#세션 이용
#클라이언트와 웹 서버간에 통신 연결에서 두 개체의 활성화된 접속을 뜻합니다.
class Cart(object):
    def __init__(self, request): #초기화 작업
        self.session = request.session #세션 정보 전달
        cart = self.session.get(settings.CART_ID) #settings의 카드 아이디
        if not cart:
            cart = self.session[settings.CART_ID] = {} #새로운 딕셔너리 추가
        self.cart = cart #현재 카트 불러오기
        self.coupon_id=self.session.get('coupon_id')


    def __len__(self): #iterate같은 거 쓸때 몇개나 있어. 카트 제품의 것을 다 더해줄게야
        return sum(product['quantity'] for product in self.cart.values())

    def __iter__(self): #어떤 요소들을 건네줄거야?
        item_ids = self.cart.keys() #제품 번호 목록 가져옴

        items = Item.objects.filter(id__in=item_ids) #이 아이디에만 있는 거 줘

        for item in items:
            self.cart[str(item.id)]['item'] = item

        for product in self.cart.values(): # 장바구니에 있는 것 하나씩 꺼냄
            int(product['item_price'])
            product['total_price'] = int(product['item_price']) * product['quantity']

            yield product #데이터베이스에서 가져오고 계속해서 위와 계산함


    def add(self, item, quantity=1, is_update=False): #제품 장바구니에 집어넣기
        item_id = str(item.id) #is_update=>장바구니에 담을 때는 update x. 수정할 때 update
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
        if item_id in self.cart: #있으면 지워버려
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
        return self.get_item_total() - self.get_discount_total() + 2500


