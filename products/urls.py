from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore 
from .views import ProductViewSet, CategoryViewSet, SubcategoryViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category-products/', CategoryViewSet.as_view({'get': 'products'})),
    path('products/<int:pk>/similar/', ProductViewSet.as_view({'get': 'similar'}), name='product-similar'),
    path('categories/delete_category/<int:pk>/', CategoryViewSet.as_view({'delete': 'delete_category'}), name='delete_category'),
    path('subcategories/delete_subcategory/<int:pk>/', SubcategoryViewSet.as_view({'delete': 'delete_subcategory'}), name='delete_subcategory'),
    path('products/delete_product/<int:pk>/', ProductViewSet.as_view({'delete': 'delete_product'}), name='delete_product'),
    path('products/update_product/<int:pk>/', ProductViewSet.as_view({'put': 'update_product'}), name='update_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
