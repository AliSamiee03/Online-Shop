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


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_products', 'paid', 'status', 'final_price', 'discount']
        read_only_fields = ['id', 'final_price', 'order_products']

    def validate_status(self, value):
        if self.instance and self.instance.status != value:
            if value in ['preparing', 'shipped', 'delivered'] and self.instance.order_products.count() == 0:
                raise serializers.ValidationError("An order without an item cannot reach this status.")
        return value