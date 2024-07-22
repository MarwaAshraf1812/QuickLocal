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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
