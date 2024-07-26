from rest_framework import viewsets #type: ignore	
from rest_framework.response import Response #type: ignore	
from rest_framework.decorators import action #type: ignore	
from rest_framework import status #type: ignore	
from cart.serializers import CartSerializer	
from cart.models import CartItem	
from products.models import Product	
from .models import Order, OrderItem	
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer	
import stripe #type: ignore	
from django.conf import settings	

stripe.api_key = settings.STRIPE_SECRET_KEY	

class OrderViewSet(viewsets.ViewSet):	
    """	
    A ViewSet for handling orders, including creation,	
    retrieval, updating, and deletion of orders.	
    """	
    @action(detail=False, methods=['post'])	
    def create_order(self, request) -> Response:	
        """	
        Create an order from cart items and return the total amount, total items, and Stripe client secret.	
        	
        Args:	
            request (Request): The request object containing order data.	
        Returns:	
            Response: A response object containing the order details and Stripe client secret.	
        """	
        serializer = CreateOrderSerializer(data=request.data)	
        serializer.is_valid(raise_exception=True)	
        order_data = serializer.validated_data	

        stripe_token = order_data.pop('stripe_token')	
        user = request.user	

        # Extract items from the user's cart	
        cart_items = CartItem.objects.filter(cart__user=user)	
        if not cart_items.exists():	
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)	

        # Create Order object	
        order = Order.objects.create(user=user, **order_data)	

        total_amount = 0	
        total_items = 0	
        order_items = []	

        for item in cart_items:	
            # Create OrderItem object for each cart item	
            order_item = OrderItem.objects.create(	
                order=order,	
                product=item.product,	
                quantity=item.quantity,	
                price=item.product.price  # Assuming price comes from product	
            )	
            total_amount += order_item.quantity * order_item.price	
            total_items += order_item.quantity	

            # Add to the list of order items	
            order_items.append({	
                'product': item.product.id,	
                'quantity': item.quantity,	
                'price': item.product.price	
            })	

        order.total_amount = total_amount	
        order.save()	

        # Create a Stripe PaymentIntent	
        try:	
            intent = stripe.PaymentIntent.create(	
                amount=int(order.total_amount * 100),  # Stripe amount is in cents	
                currency='usd',	
                payment_method=stripe_token,  # Attach payment method	
                confirm=True,  # Confirm the payment	
                metadata={'order_id': order.id},	
                automatic_payment_methods={	
                    'enabled': True,	
                    'allow_redirects': 'never'  # Disable redirects	
                },	
            )	
        except stripe.error.StripeError as e:	
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)	

        # Update order status upon successful payment)	
        if intent.status == 'succeeded':	
            order.order_status = 'paid'	
            order.save()	
            # Clear the cart	
            CartItem.objects.filter(cart__user=user).delete()	

        # Serialize the order	
        order_serializer = OrderSerializer(order)	
        return Response({	
            'order': order_serializer.data,	
            'total_amount': str(total_amount),	
            'total_items': total_items,	
            'order_items': order_items,  # Include the order items in the response	
            'client_secret': intent.client_secret	
        }, status=status.HTTP_201_CREATED)	

    @action(detail=False, methods=['get'])	
    def user_orders(self, request) -> Response:	
        """	
        Retrieve all orders for the authenticated user.	
        Args:	
            request (Request): The request object.	
        Returns:	
            Response: A response object containing the user's orders.	
        """	
        if not request.user.is_authenticated:	
            return Response({'message': 'you are not loged in !'}, status=status.HTTP_401_UNAUTHORIZED)	

        user = request.user	
        orders = Order.objects.filter(user=user)	
        serializer = OrderSerializer(orders, many=True)	
        return Response(serializer.data)	

    @action(detail=True, methods=['get'])	
    def order_detail(self, request, pk=None) -> Response:	
        """	
        Retrieve a specific order by its ID.	
        Args:	
            request (Request): The request object.	
            pk (str): The primary key of the order.	
        Returns:	
            Response: A response object containing the order details.	
        """	
        try:	
            order = Order.objects.get(id=pk)	
        except Order.DoesNotExist:	
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)	

        serializer = OrderSerializer(order)	
        return Response(serializer.data)	

    @action(detail=False, methods=['get'])	
    def list_all_orders(self, request) -> Response:	
        """	
        Retrieve all orders.	
        Args:	
            request (Request): The request object.	
        Returns:	
            Response: A response object containing all orders.	
        Retrieve all orders (Admin only).	
        """	
        orders = Order.objects.all()	
        serializer = OrderSerializer(orders, many=True)	
        return Response(serializer.data)	

    @action(detail=True, methods=['put'])	
    def update_order(self, request, pk=None) -> Response:	
        """	
        Update an existing order.	
        Args:	
            request (Request): The request object containing order data.	
            pk (str): The primary key of the order.	
        Returns:	
            Response: A response object containing the updated order details.	
        """	
        try:	
            order = Order.objects.get(id=pk)	
        except Order.DoesNotExist:	
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)	

        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)	
        if serializer.is_valid():	
            serializer.save()	
            return Response(serializer.data, status=status.HTTP_200_OK)	
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	

    @action(detail=False, methods=['delete'])	
    def delete_order(self, request, pk=None) -> Response:	
        """	
        Delete an order by its ID.	
        Args:	
            request (Request): The request object.	
            pk (str): The primary key of the order.	
        Returns:	
            Response: A response object indicating whether the deletion was successful.	
        """	
        try:	
            order = Order.objects.get(id=pk)	
            order.delete()	
            return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)	
        except Order.DoesNotExist:	
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)	


    @action(detail=True, methods=['put'])	
    def update_order_status(self, request, pk=None) -> Response:	
        """	
        Update the status of an existing order.	
        Args:	
            request (Request): The request object containing the updated order status.	
            pk (str): The primary key of the order.	
        Returns:	
            Response: A response object indicating whether the status was updated successfully	
        """	
        try:	
            order = Order.objects.get(pk=pk)  # Direct query for debugging	
            order_status = request.data.get('order_status')	
            if order_status:	
                order.order_status = order_status	
                order.save()	
                return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)	
            return Response({'error': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)	
        except Order.DoesNotExist:	
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)	
        except Exception as e:	
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)	
