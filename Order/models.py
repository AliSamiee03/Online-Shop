from itertools import product
from django.db import models
from Product.models import Product
from Account.models import CustomUser
from django.core.validators import MinValueValidator
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICE = [
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('pending_payment', 'Pending Payment'),
    ]


    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='orders')
    item = models.ManyToManyField('Product.Product')
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=55, choices=STATUS_CHOICE)
    final_price = models.PositiveBigIntegerField()
    discount = models.ForeignKey('Discount', on_delete=models.SET_DEFAULT, default=0)

    def calculate_final_price(self):
        order_product = self.order_product.all()

        total = sum(op.product.price * op.quantity for op in order_product)
        self.final_price = total
        self.save()


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_product')
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Discount(models.Model):
    code = models.CharField(max_length=12)
    title = models.CharField(max_length=55)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='discounts')
    due_date = models.DateTimeField(validators=[MinValueValidator(timezone.now())])