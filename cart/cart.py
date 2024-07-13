from django.conf import settings
from decimal import Decimal
from products.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        # You store the current session to make it accessible to the other methods of the Cart class
        self.session = request.session

        # Try to get the cart from the current session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        # If there is no cart in the session, you create an empty cart by setting an empty dictionary in the session.
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        """"
        Add a product to the cart or update its quantity.
        """
        #  convert the product ID into a string because Django uses JSON to serialize session data
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity' : 0,
                                        'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as modified to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
        self.session.modified = True