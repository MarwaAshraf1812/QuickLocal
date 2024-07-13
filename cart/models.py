from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    """- This model will represent the shopping cart itself.
       It will have a one-to-one relationship with the user model.
       This is Model is needed to track of which cart belongs to which user,
       providing a way to store cart-related information tied to a user.

       - Purpose: To link the cart to a user and maintain
       cart creation and update timeStimps.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'

class CartItem(models.Model):
    """ - This model will represent the items in the cart.Linking the cart and the product.
        - This model  represents the items in the cart,
        which will be linked to the cart and product models.

        - This model is needed to store the quantity of a product in the cart,
        the price of the product at the time it was added to the cart,
        and the timestamps of when the item was created and last updated.

        - To represent and manage individual products in a cart,
        keeping track of the quantity of each product,
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user}'s Cart"
    
    def get_total_price(self):
        return self.quantity * self.price
    
