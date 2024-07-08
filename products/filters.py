# import django_filters
# from .models import Product

# class ProductFilter(django_filters.FilterSet):
#     product_name = 
#     price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
#     price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
#     category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
#     rating_min = django_filters.NumberFilter(field_name="rating", lookup_expr='gte')

#     class Meta:
#         model = Product
#         fields = [,'price_min', 'price_max', 'category', 'rating_min']