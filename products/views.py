import logging
from rest_framework import viewsets, filters, status #type: ignore
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from django.shortcuts import get_object_or_404
from .Helper_function import apply_product_filters
from rest_framework.permissions import AllowAny #type: ignore
from vendor.permissions import IsStaffUser
from rest_framework import permissions #type: ignore

# Use logging to capture exceptions for better debugging.
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing products, including retrieval
    of similar products based on category.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'tags__name']
    ordering_fields = ['price', 'created_at']
    permission_classes = [AllowAny] 

    @action(detail=False, methods=['get'])
    def similar(self, request, pk=None) -> Response:
        """
        Retrieve similar products based on the same category.
        Optional query parameters for filtering:
        - category: Filter by category name (string)
        - name: Filter by product name (string)
        - min_price, max_price: Filter by price range (float)
        - rating: Filter by minimum rating (integer)
        - tags: Filter by tags (list of strings)
        Args:
            request (Request): The request object containing query parameters.
        Returns:
            Response: A response object containing the filtered list of similar products.
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
            logger.error(f"Error retrieving similar products: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_queryset(self):
        """
        Return a filtered queryset of products based on the vendor.
        If the user is authenticated and is a vendor, only products for that vendor are returned.
        Otherwise, all products are returned.

        Returns:
            QuerySet: A queryset of products filtered by vendor if authenticated and a vendor, or all products.
        """
        if self.request.user.is_authenticated:
            return Product.objects.filter(vendor=self.request.user.vendor)
        return Product.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsStaffUser])
    def create_product(self, request, *args, **kwargs) -> Response:
        """
        Create a new product. Only accessible by staff users who are also vendors.

        Args:
            request (Request): The request object containing product data.

        Returns:
            Response: The created product data or an error message if the user is not a vendor.
        """
        try:
            if not request.user.is_staff:
                return Response({'error': 'Only vendors can create products.'}, status=status.HTTP_403_FORBIDDEN)
            
            data = request.data.copy()
            if hasattr(request.user, 'vendor'):
                data['vendor'] = request.user.vendor.id
            else:
                return Response({'error': 'User is not a vendor.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ProductSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_product(self, request, pk=None) -> Response:
        """
        Update an existing product. Only accessible by staff users who are also vendors.

        Args:
            request (Request): The request object containing updated product data.
            pk (int): The ID of the product to be updated.

        Returns:
            Response: The updated product data or an error message if the product is not found or the user is not a vendor.
        """
        try:
            if not request.user.is_staff:
                return Response({'error': 'Only vendors can update products.'}, status=status.HTTP_403_FORBIDDEN)
            
            product = self.get_object()
            data = request.data.copy()
            if hasattr(request.user, 'vendor'):
                data['vendor'] = request.user.vendor.id
            serializer = ProductSerializer(product, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_product(self, request, pk=None) -> Response:
        """
        Delete an existing product. Only accessible by staff users who are also vendors.

        Args:
            request (Request): The request object.
            pk (int): The ID of the product to be deleted.

        Returns:
            Response: A success message if the product is deleted or an error message if the product is not found or the user is not a vendor.
        """
        try:
            if not request.user.is_staff:
                return Response({'error': 'Only vendors can delete products.'}, status=status.HTTP_403_FORBIDDEN)
            product = self.get_object()  # Retrieves the product based on pk
            product.delete()
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing categories and their associated products.
    """
    queryset = Category.objects.prefetch_related('subcategories', 'subcategories__products').all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] 

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Retrieve a specific category by its ID.
        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.
        Returns:
            Response: A response object containing the category details.
        """
        try:
            instance = self.get_object()
            serializer = CategorySerializer(instance, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        except Exception as e:
            logger.error(f"Error retrieving category: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def products(self, request):
        """
        Retrieve products for a given category and optional subcategory.
        Query parameters:
        - category: Category ID (integer, required)
        - subcategory: Subcategory ID (integer, optional)

         Args:
            request (Request): The request object containing query parameters.
        Returns:
            Response: A response object containing the list of products for the specified category and optional subcategory.
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
            logger.error(f"Error retrieving products: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def delete_category(self, request, pk=None) -> Response:
        """
        Delete a specific category by its ID.
        Args:
            request (Request): The request object.
            pk (int): The ID of the category to delete.
        Returns:
            Response: A response object indicating success or failure.
        """
        try:
            category = self.get_object()
            category.delete()
            return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting category: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing subcategories.
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Retrieve a specific subcategory by its ID.
        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.
        Returns:
            Response: A response object containing the subcategory details.
        """
        try:
            instance = self.get_object()
            serializer = SubCategorySerializer(instance)
            return Response(serializer.data)
        except SubCategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=404)
        except Exception as e:
            logger.error(f"Error retrieving subcategory: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def delete_subcategory(self, request, pk=None) -> Response:
        """
        Delete a specific subcategory by its ID.
        Args:
            request (Request): The request object.
            pk (int): The ID of the subcategory to delete.
        Returns:
            Response: A response object indicating success or failure.
        """
        try:
            subcategory = self.get_object()
            subcategory.delete()
            return Response({'message': 'Subcategory deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except SubCategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting subcategory: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
