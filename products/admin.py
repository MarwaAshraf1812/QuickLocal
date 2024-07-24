from django.contrib import admin

from .models import Category, Product, SubCategory
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
