from rest_framework import serializers #type: ignore
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer
from django.shortcuts import get_object_or_404

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'total_price', 'total_items', 'items']

    def get_total_price(self, obj):
        return obj.get_total_cost()

    def get_total_items(self, obj):
        return obj.items.count()