from django.db import models
from taggit.managers import TaggableManager # type: ignore

def category_image_path(instance, filename):
    return "categories/{}/{}/{}".format(instance.id, instance.name, filename)

def product_image_path(instance, filename):
    return "products/{}/{}/{}".format(instance.category,instance.name, filename)

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=category_image_path, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    productInformation = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0) # Quantity in stock
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=7, default='#FFFFFF', blank=True)
    size = models.CharField(max_length=100, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def update_rating(self):
        ratings = self.product_ratings.all()
        if ratings.exists():
            self.rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
        else:
            self.rating = None
        self.save()
