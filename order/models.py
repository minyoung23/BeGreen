from itertools import product

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from coupon.models import Coupon

class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name='구매자', null=True)
    email = models.EmailField()
    address_country = models.CharField(max_length=250, verbose_name='도시 주소', null=True)
    address_house = models.CharField(max_length=250, verbose_name='주거지 주소', null=True)
    postal_code = models.CharField(max_length=20, verbose_name='우편번호')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_item(self):
        return sum(product.get_product_price() for product in self.products.all())

    def get_total_price(self):
        total_item = self.get_total_item()
        return total_item - self.discount


from shop.models import Item

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='order_items')
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_product_price(self):
        return self.price * self.quantity

