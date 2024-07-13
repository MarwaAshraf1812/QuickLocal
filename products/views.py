from rest_framework import viewsets, filters, status #type: ignore
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from django.shortcuts import get_object_or_404
from .Helper_function import apply_product_filters

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'tags__name']
    ordering_fields = ['price', 'created_at']

    @action(detail=False, methods=['get'])
    def similar(self, request, pk=None):
        """
        Retrieve similar products based on the same category.
        Optional query parameters for filtering:
        - category: Filter by category name (string)
        - name: Filter by product name (string)
        - min_price, max_price: Filter by price range (float)
        - rating: Filter by minimum rating (integer)
        - tags: Filter by tags (list of strings)
        """
        try:
            product = self.get_object()
            similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)
            similar_products = apply_product_filters(similar_products, request.query_params)
            serializer = ProductSerializer(similar_products, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories', 'subcategories__products').all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = CategorySerializer(instance, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def products(self, request):
        """
        Retrieve products for a given category and optional subcategory.
        Query parameters:
        - category: Category ID (integer, required)
        - subcategory: Subcategory ID (integer, optional)
        """
        category_id = request.query_params.get('category')
        if not category_id:
            return Response({'error': 'Category ID is required'}, status=400)

        try:  
            category = get_object_or_404(Category, id=category_id)
            products = Product.objects.filter(category__category=category)
            subcategory_id = request.query_params.get('subcategory')

            if subcategory_id:
                subcategory = get_object_or_404(SubCategory, id=subcategory_id)
                products = products.filter(category=subcategory)

            product_serializer = ProductSerializer(products, many=True)
            return Response({'products': product_serializer.data})
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        except SubCategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SubCategorySerializer(instance)
            return Response(serializer.data)
        except SubCategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
