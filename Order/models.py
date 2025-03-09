from itertools import product
from django.db import models
from Product.models import Product
from Account.models import CustomUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_final_price()

    def __str__(self):
        return f"{self.id} - {self.order} - {self.product}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('pending_payment', 'Pending Payment'),
    ]

    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='orders')
    item = models.ManyToManyField('Product.Product', through=OrderProduct)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=55, choices=STATUS_CHOICES)
    final_price = models.PositiveIntegerField(default=0)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_final_price(self):
        order_products = self.order_products.all()

        if not order_products:
            self.final_price = 0
            self.save(update_fields=['final_price'])
            return 0

        total_price = sum(
            (op.product.price - (op.product.discount.amount if op.product.discount else 0)) * op.quantity
            for op in order_products
        )

        if self.discount:
            total_price -= self.discount.amount
            total_price = max(total_price, 0)

        if self.final_price != total_price:
            self.final_price = total_price
            self.save(update_fields=['final_price'])
        return total_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_final_price()


    def __str__(self):
        return f"{self.user} Order"


class Discount(models.Model):
    code = models.CharField(max_length=12)
    title = models.CharField(max_length=55)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='discounts')
    due_date = models.DateTimeField(validators=[MinValueValidator(timezone.now())])

    def __str__(self):
        return f"{self.title} - {self.amount}"

