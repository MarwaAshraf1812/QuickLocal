from rest_framework import viewsets, status #type: ignore
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework.permissions import IsAuthenticated #type: ignore
from django.shortcuts import get_object_or_404 
from products.models import Product
from .cart import CartManager
from .serializers import CartItemSerializer
from typing import Optional

class CartViewSet(viewsets.GenericViewSet, viewsets.ViewSet):
    """
    A viewset for managing shopping cart operations.
    Requires authentication for all actions.
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add-to-cart/(?P<product_id>[^/.]+)')
    def add_to_cart(self, request, product_id: Optional[int] = None) -> Response:
        """
        Custom action to add a product to the cart.

        Parameters:
        - product_id: Primary key of the product instance to add to cart

        POST data:
        - quantity: Optional quantity of the product to add (default is 1)

        Returns:
        - Response indicating the result of adding the product to cart
        """
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity', 1)
        
        cart_manager = CartManager(request)
        cart_manager.add(product=product, quantity=quantity)

        return Response({"message": "Product added to cart successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='list-cart-items')
    def list_cart_items(self, request) -> Response:
        """
        Retrieve all items in the cart.

        Returns:
        - Serialized cart items, total items count, and total price
        """
        cart_manager = CartManager(request)
        cart_items = cart_manager.get_items()

        page = self.paginate_queryset(cart_items)
        if page is not None:
            serializer = CartItemSerializer(page, many=True)
            response_data = {
                'items': serializer.data,
                'total_items': cart_manager.__len__(),
                'total_price': cart_manager.get_total_price()
            }
            return self.get_paginated_response(response_data)

        serializer = CartItemSerializer(cart_items, many=True)
        response_data = {
            'items': serializer.data,
            'total_items': cart_manager.__len__(),
            'total_price': cart_manager.get_total_price()
        }
        return Response(response_data)

    action(detail=False, methods=['post'], url_path='remove-from-cart/(?P<product_id>[^/.]+)')
    def remove_from_cart(self, request, product_id=None):
        """
        Remove a product from the cart.

        Parameters:
        - product_id: ID of the product to remove

        Returns:
        - Response with success message
        """
        product = get_object_or_404(Product, id=product_id)
        cart_manager = CartManager(request)
        removed = cart_manager.remove(product)
        
        if removed:
            return Response({"message": "Product removed from cart successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='update-cart-item/(?P<product_id>[^/.]+)')
    def update_cart_item(self, request, product_id=None):
        """
        Update quantity of a product in the cart.

        Parameters:
        - product_id: ID of the product to update
        - quantity: New quantity of the product in the cart

        Returns:
        - Response with success message or error message if the product was not found in the cart
        """
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({"error": "Quantity parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid quantity value"}, status=status.HTTP_400_BAD_REQUEST)

        cart_manager = CartManager(request)
        try:
            cart_manager.update(product, quantity)
            return Response({"message": "Cart item updated successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='clear-cart')
    def clear_cart(self, request):
        """
        Clear the cart by removing all items.

        Returns:
        - Response with success message
        """
        cart_manager = CartManager(request)
        if not cart_manager:
            return Response({"error": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart_manager.clear()
            return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)
