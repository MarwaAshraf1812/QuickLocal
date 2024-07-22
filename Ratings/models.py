from django.db import models
from django.conf import settings
from products.models import Product


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
<<<<<<< HEAD
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
=======
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
>>>>>>> 1b8fa9596cb54cab2ffe241e9a15f890789523c7
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating}'

    class Meta:
        unique_together = ('user', 'product')


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.review[:30]}'

    class Meta:
        unique_together = ('user', 'product')
