from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore
from cart.views import CartViewSet

app_name = 'cart'

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart') 

urlpatterns = [
    path('', include(router.urls)),
    path('list_cartItems', CartViewSet.as_view({'get': 'list'}), name='get_cart'),
    path('add_to_cart/<int:pk>/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', CartViewSet.as_view({'post': 'remove'}), name='remove_from_cart'),
    path('clear_cart/', CartViewSet.as_view({'post': 'clear'}), name='clear_cart'),
]
