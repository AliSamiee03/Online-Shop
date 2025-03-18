from rest_framework import serializers
from .models import Product, Category, DiscountCategory, Comment

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'model', 'price', 'memory', 'RAM', 'cpu', 'camera', 'discount']

