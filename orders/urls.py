from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore
from .views import OrderViewSet
from cart.views import CartViewSet  # Assuming you have a CartViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cart', CartViewSet, basename='cart')  # Assuming you have a CartViewSet

urlpatterns = [
    path('', include(router.urls)),
    path('create_order/', OrderViewSet.as_view({'post': 'create_order'}), name='create_order'),
    path('list_all_orders/', OrderViewSet.as_view({'get': 'list_all_orders'}), name='list_all_orders'),
    path('order_detail/<int:pk>/', OrderViewSet.as_view({'get': 'order_detail'}), name='order_detail'),
    path('update_order/<int:pk>/', OrderViewSet.as_view({'put': 'update_order'}), name='update_order'),
    path('delete_order/<int:pk>/', OrderViewSet.as_view({'delete': 'delete_order'}), name='delete_order'),
]
