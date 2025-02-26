from itertools import product
from django.db import models
from Product.models import Product
from Account.models import CustomUser
from django.core.validators import MinValueValidator
from django.utils import timezone

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orderproduct')
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('pending_payment', 'Pending Payment'),
    ]

    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='orders')
    item = models.ManyToManyField('Product.Product', through=OrderProduct, related_name='orders')
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=55, choices=STATUS_CHOICES)
    final_price = models.PositiveIntegerField(default=0)  # یا DecimalField
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def calculate_final_price(self):
        order_products = self.orderproduct.all()  # یا از related_name استفاده کنید
        total = sum(
            (op.product.price - (op.product.discount or 0)) * op.quantity
            for op in order_products
        )
        self.final_price = total
        self.save()





class Discount(models.Model):
    code = models.CharField(max_length=12)
    title = models.CharField(max_length=55)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='discounts')
    due_date = models.DateTimeField(validators=[MinValueValidator(timezone.now())])