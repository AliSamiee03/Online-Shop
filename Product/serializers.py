from rest_framework import serializers
from .models import Product, Category, DiscountCategory, Comment

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'model', 'price', 'memory', 'RAM', 'cpu', 'camera', 'discount']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'discount']


class DiscountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCategory
        fields = ['name', 'validityـdate', 'amount']
        read_only_fields = ['validitydate']


