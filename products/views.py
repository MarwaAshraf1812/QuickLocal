from rest_framework import viewsets, filters
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'tags__name']
    ordering_fields = ['price', 'created_at']

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        product = self.get_object()
        similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)

        # Apply filters
        name = request.query_params.get('name')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        tags = request.query_params.getlist('tags')

        if name:
            similar_products = similar_products.filter(name__icontains=name)
        if price_min:
            similar_products = similar_products.filter(price__gte=price_min)
        if price_max:
            similar_products = similar_products.filter(price__lte=price_max)
        if tags:
            for tag in tags:
                similar_products = similar_products.filter(tags__name=tag)

        serializer = ProductSerializer(similar_products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Added prefetch_related('subcategories', 'products')
    to the queryset attribute. This prefetches related
    subcategories and products for each category,
    optimizing database queries when serializing data.
    """
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CategorySerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category__category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        subcategory = self.get_object()
        products = Product.objects.filter(category=subcategory)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)