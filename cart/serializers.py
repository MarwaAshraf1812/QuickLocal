from rest_framework import serializers #type: ignore
from products.serializers import ProductSerializer
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

    def get_product(self, obj):
        # Assuming obj.product is a ForeignKey to Product model
        return ProductSerializer(obj.product).data

    
class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_items = serializers.IntegerField(source='__len__')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_total_price')
