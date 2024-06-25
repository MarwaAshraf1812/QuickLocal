from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from .views import ProductViewSet, OrderViewSet, ProductDetailsViewSet, OrderItemViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'categories', CategoryViewSet)



urlpatterns = [
    path('', include(router.urls)),
]
