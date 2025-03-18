from rest_framework import serializers
from .models import Order, OrderProduct, Discount
from Product.models import Product

class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'quantity']
        read_only_fields = ['id']

    def validate(self, data):
        order = data['order']
        if order.status in ['preparing', 'shipped', 'delivered']:
            raise serializers.ValidationError("You cannot add items to an order that is being prepared or closed.")
        return data

    def create(self, validated_data):
        order = validated_data['order']
        return OrderProduct.objects.create(**validated_data)