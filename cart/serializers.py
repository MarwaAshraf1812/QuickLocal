from decimal import Decimal
from rest_framework import serializers #type: ignore
from products.models import Product
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_product(self, obj):
        # Assuming 'product' is a nested object in 'self.cart'
        return ProductSerializer(obj['product']).data

    
class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_items = serializers.IntegerField(source='__len__')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_total_price')
