from rest_framework import viewsets, status #type: ignore
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework.permissions import IsAuthenticated #type: ignore
from django.shortcuts import get_object_or_404 
from products.models import Product
from .cart import CartManager
from .serializers import CartItemSerializer, CartSerializer

class CartViewSet(viewsets.ViewSet):
    """
    A viewset for managing shopping cart operations.
    Requires authentication for all actions.
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request, product_id=None):
        """
        Custom action to add a product to the cart.

        Parameters:
        - pk: Primary key of the product instance to add to cart

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

    @action(detail=False, methods=['get'])
    def list_cartItems(self, request):
        """
        Retrieve all items in the cart.

        Returns:
        - Serialized cart items, total items count, and total price
        """
        cart_manager = CartManager(request)
        cart_items = cart_manager.get_items()

        page = self.paginate_queryset(cart_items)
        if page is not None:
            serializer = CartSerializer({
                'items': page,
                'total_items': cart_manager.__len__(),
                'total_price': cart_manager.get_total_price()
            })
            return self.get_paginated_response(serializer.data)

        serializer = CartSerializer({
            'items': cart_items,
            'total_items': cart_manager.__len__(),
            'total_price': cart_manager.get_total_price()
        })
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
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
        cart_manager.remove(product)
        return Response({"message": "Product removed from cart successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_product(self, request, product_id=None):
        """
        Update the quantity of a product in the cart.

        Parameters:
        - product_id: ID of the product to update
        - quantity: New quantity of the product

        Returns:
        - Response with success message
        """
        product = get_object_or_404(Product, id=product_id)
        cart_manager = CartManager(request)
        cart_manager.update(product, quantity=request.data.get('quantity', 1))
        return Response({"message": "Product updated in cart successfully"}, status=status.HTTP_200_OK)

    def clear_cart(self, request):
        """
        Clear the cart by removing all items.

        Returns:
        - Response with success message
        """
        cart_manager = CartManager(request)
        cart_manager.clear()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)
