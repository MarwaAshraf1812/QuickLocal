from rest_framework import serializers #type: ignore
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer
from django.shortcuts import get_object_or_404

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'total_amount', 'total_items']

    def get_total_amount(self, obj):
        return str(obj.total_amount)  # Ensure the amount is returned as a string

    def get_total_items(self, obj):
        return obj.items.count()

class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class CreateOrderSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=250)
    postal_code = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=100)
    stripe_token = serializers.CharField(max_length=255)

    def validate_items(self, value):
        # Additional validation for items if needed
        return value
    
    def validate(self, data):
        if not data.get('stripe_token'):
            raise serializers.ValidationError({'stripe_token': 'Payment method is required'})
        return data
    
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

    def validate(self, data):
        # Additional validation if needed
        return data