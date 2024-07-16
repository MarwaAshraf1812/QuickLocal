from django.conf import settings
from decimal import Decimal
from products.models import Product
from .models import Cart, CartItem

class CartManager:
    """
    - Initializes the cart using the session and user information from the request.
    - To provide a way to manage the cart operations, such as adding and removing products,
    and calculating the total price of the items in the cart.
    """
    def __init__(self, request):
        # You store the current session to make it accessible to the other methods of the Cart class
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        self.cart = self._get_or_create_cart()


    def _get_or_create_cart(self):
        if self.user:
            cart = Cart.objects.get_or_create(user=self.user)
        else:
            cart_id = self.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id).first()
            else:
                cart = Cart.objects.create()
                self.request.session['cart_id'] = cart.id
        return cart
    
    def add(self, product, quantity=1, overide_quantity=False):
        cart_item = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'price': product.price, 'quantity': 0}
            )
        if overide_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

    def remove(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    
    def update(self, product, quantity):
        cart_item = CartItem.objects.get(cart=self.cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

    def __len__(self):
        return sum(item.quantity for item in self.cart.items.all())

    def get_items(self):
        return self.cart.items.all()
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.get_items())
    
    def clear(self):
        self.cart.items.all().delete()