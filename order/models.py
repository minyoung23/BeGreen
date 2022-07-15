from itertools import product

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator #어떤 값이 들어갈지 카운팅하게 도와줌
from coupon.models import Coupon

#주문서 개념의 모델
class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name='구매자', null=True)
    email = models.EmailField(verbose_name='이메일')
    address = models.CharField(max_length=250, verbose_name='주소', null=True)
    tel = models.CharField(max_length=30, verbose_name='휴대폰 번호', null=True)
    notice=models.CharField(max_length=150, verbose_name='배송시 유의사항', null=True)
    postal_code = models.CharField(max_length=20, verbose_name='우편번호')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_item(self):
        return sum(product.get_product_price() for product in self.products.all())

    def get_total_price(self):
        total_item = self.get_total_item()
        return (total_item - self.discount) +2500


#주문서에 들어가는 상품 모델
from shop.models import Item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products') #위의 tota_product에서 products임
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='order_items') #item입장에서 위의 order을 order_items로 부름
    item_price = models.IntegerField() #product에 있는 price 모델
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_product_price(self): #위의 get_item_price에 연결됨
        return self.item_price * self.quantity

#주문서를 받아서 그 주문에 해당하는 고유의 merchant_order_id의 생성
#새로 transaction 이 생겻을 때 관련 order정보를 갖게 함
#매니저 정보를 customize 함
import hashlib, datetime
from .iamport import payments_prepare, find_transaction
class OrderTransactionManager(models.Manager):
    #success는 결제 여부 판단.
    def create_new(self,order,amount,success=None,transaction_status=None):
        if not order: #order 정보 없을 때
            raise ValueError("주문 오류")

        #sha1는 암호화 방식. hex방식을 바꿈
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        email_hash = str(order.email).split("@")[0]
        datetime_hash=str(datetime.datetime.now())
        final_hash = hashlib.sha1((order_hash + email_hash + datetime_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = str(final_hash) #동영상 강의에서 변경. 74강

        payments_prepare(merchant_order_id,amount)

        #매니저에게다가 transaction 정보 넣음
        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error",e)

        return transaction.merchant_order_id

#iamport의 영수증을 가져오는 함수
    def get_transaction(self,merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid': #돈이 냈으면 result 정보 넘김
            return result
        else:
            return None


#결제 정보 모델
class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True,blank=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True,blank=True) #결제 상태를 받아옴
    type = models.CharField(max_length=120,blank=True) #
    created = models.DateTimeField(auto_now_add=True,auto_now=False)

    #objects에 매니저 접근 가능
    objects = OrderTransactionManager()

    #출력했을 때 나오는 문자열
    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']

#db 영수증이 생성될 때 iamport 영수증과 맞는지 점검하는 함수
def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id: #모델에서 instace save
        #ordertransaction에서 save가 일어났을 때, merchant_order_id와 transaciton의 merchant_order_id 정보를 가지고 와보자
        iamport_transaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)

        merchant_order_id = iamport_transaction['merchant_order_id']
        imp_id = iamport_transaction['imp_id']
        amount = iamport_transaction['amount']

        #결제정보 가져온 것을 비교하기
        local_transaction = OrderTransaction.objects.filter(merchant_order_id = merchant_order_id, transaction_id = imp_id,amount = amount).exists()

        #위에 둘 다 없거나 둘 중에 하나가 없거나
        if not iamport_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")

# 결제 정보가 생성된 후에 호출할 함수를 연결해준다.
#post save후 validation 여부를 확인할 게. 모든 post save 후
from django.db.models.signals import post_save
post_save.connect(order_payment_validation,sender=OrderTransaction)

