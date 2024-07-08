from rest_framework import viewsets, filters #type: ignore
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from django.shortcuts import get_object_or_404

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
        category = request.query_params.get('category')
        name = request.query_params.get('name')
        price_min = request.query_params.get('min_price')
        price_max = request.query_params.get('max_price')
        rating = request.query_params.get('rating')
        tags = request.query_params.getlist('tags')

        if category:
            similar_products = similar_products.filter(category__name__icontains=category)
        if name:
            similar_products = similar_products.filter(name__icontains=name)
        if price_min:
            similar_products = similar_products.filter(price__gte=price_min)
        if price_max:
            similar_products = similar_products.filter(price__lte=price_max)
        if rating:
            similar_products = similar_products.filter(rating__gte=rating)
        if tags:
            for tag in tags:
                similar_products = similar_products.filter(tags__name=tag)

        serializer = ProductSerializer(similar_products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories', 'subcategories__products').all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CategorySerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def products(self, request):
        category_id = request.query_params.get('category')
        subcategory_id = request.query_params.get('subcategory')

        category = get_object_or_404(Category, id=category_id)
        subcategories = category.subcategories.all()
        products = Product.objects.filter(category__category=category)

        if subcategory_id:
            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
            products = products.filter(category=subcategory)

        product_serializer = ProductSerializer(products, many=True)
        return Response({
            'products': product_serializer.data
        })

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SubCategorySerializer(instance)
        return Response(serializer.data)
