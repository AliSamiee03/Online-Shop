from django.contrib import admin
from .models import Product, DiscountCategory, Category, Comment
# Register your models here.

admin.site.register([Product, DiscountCategory, Category, Comment])