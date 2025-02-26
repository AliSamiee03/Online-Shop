from django.contrib import admin
from .models import Order, OrderProduct, Discount
# Register your models here.

admin.site.register([Order, OrderProduct, Discount])