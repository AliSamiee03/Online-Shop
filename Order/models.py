from itertools import product

from django.db import models
from Product.models import Product
from Account.models import CustomUser

class Order(models.Model):
    STATUS_CHOICE = [
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('pending_payment', 'Pending Payment'),
    ]


    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='orders')
    item = models.ManyToManyField('Product')
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICE)
    final_price = models.PositiveBigIntegerField()
    discount = models.ForeignKey('Discount', on_delete=models.SET_DEFAULT, default=0)


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_product')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_product')
    product_count = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        total = product_count * product.price
        self.total_price = total
        self.save()