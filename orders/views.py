from rest_framework import viewsets, status #type: ignore
from rest_framework.decorators import action #type: ignore
from rest_framework.permissions import IsAuthenticated #type: ignore
from rest_framework.response import Response #type: ignore
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.cart import CartManager
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_order(self, request, *args, **kwargs):
        # Extract data from the request
        cart = request.data.get('cart', [])
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        address = request.data.get('address')
        postal_code = request.data.get('postal_code')
        city = request.data.get('city')

        # Validate the cart
        if not cart:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Order instance
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            postal_code=postal_code,
            city=city,
            paid=False  # Set to True if payment has been processed
        )

        # Create OrderItems for each cart item
        for item in cart:
            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {item["product_id"]} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['quantity']
            )

        # Optionally clear the cart
        cart_manager = CartManager(request)
        cart_manager.clear()

        # Serialize and return the created order
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        # List all orders for the current user
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.user != request.user:
            return Response({'error': 'Not authorized to view this order'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
