from rest_framework import viewsets, status #type: ignore
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from django.shortcuts import get_object_or_404
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from .serializers import CartSerializer

class CartViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()
    
    @action(detail=True, methods=['get'])
    def cartDetails(self, request):
        cart = Cart(request)
        serializer = CartSerializer({
            'items': list(cart),
            'total_items': cart.__len__(),
            'total_price': cart.get_total_price(),
        })
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def addToCart(self, request, product_id=None):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        
        # Extract quantity and override from request data
        quantity = int(request.data.get('quantity', 1))  # Default to 1 if not provided
        override = bool(request.data.get('override', False))
        
        cart.add(
            product=product,
            quantity=quantity,
            override_quantity=override
        )
        
        return Response({"message": "Product added to cart successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def removeFromCart(self, request, product_id=None):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return Response({"message": "Product removed from cart successfully"}, status=status.HTTP_200_OK)
