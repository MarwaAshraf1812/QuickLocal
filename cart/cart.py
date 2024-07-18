from .models import Cart, CartItem

class CartManager:
    """
    Manages the cart operations such as adding and removing products,
    and calculating the total price of the items in the cart.
    """
    def __init__(self, request):
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        self.cart = self._get_or_create_cart()

    def _get_or_create_cart(self):
        if self.user:
            cart, created = Cart.objects.get_or_create(user=self.user)
        else:
            cart_id = self.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id).first()
            if not cart:
                cart = Cart.objects.create()
                self.session['cart_id'] = cart.id
        return cart

    def add(self, product, quantity=1, override_quantity=False):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        if not created:
            if override_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

    def remove(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            cart_item.delete()
            return True  # Indicate success
        except CartItem.DoesNotExist:
            return False  # Indicate that the item was not found in the cart

    def update(self, product, quantity):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            raise ValueError("Item does not exist in the cart.")

    def __len__(self):
        return sum(item.quantity for item in self.cart.cartitem_set.all())

    def get_items(self):
        return self.cart.cartitem_set.all()

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.get_items())

    def clear(self):
        self.cart.cartitem_set.all().delete()
