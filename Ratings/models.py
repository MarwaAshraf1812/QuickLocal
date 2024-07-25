from django.db import models
from django.conf import settings
from products.models import Product


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating}'

    class Meta:
        unique_together = ('user', 'product')


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    review = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True, related_name='review_rating')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.review[:30]}'

    class Meta:
        unique_together = ('user', 'product')
