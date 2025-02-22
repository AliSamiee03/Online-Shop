from django.db import models
from rest_framework.authtoken.admin import User
from Account.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.IntegerField()
    memory = models.IntegerField()
    RAM = models.IntegerField()
    cpu = models.CharField(max_length=100)
    camera = models.CharField(max_length=100)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, null=True, blank=True, related_name='category')

class Discount(models.Model):
    name = models.CharField(max_length=100)
    validityـdate = models.DateField()
    amount = models.IntegerField()
    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    description = models.TextField()
    def __str__(self):
        return f"Comment {self.author} for {self.product}"