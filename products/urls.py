from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, SubCategoryViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet) 

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/similar/', ProductViewSet.as_view({'get': 'similar'}), name='product-similar'),
    path('categories/<int:category_id>/subcategories/', SubCategoryViewSet.as_view({'get': 'list'}), name='category-subcategories'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
