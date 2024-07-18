from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore
from cart.views import CartViewSet

app_name = 'cart'

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart') 

urlpatterns = [
    path('', include(router.urls)),
    path('list-cart-items/', CartViewSet.as_view({'get': 'list_cart_items'}), name='list-cart-items'),
    path('update_cart_item/<int:product_id>/', CartViewSet.as_view({'post': 'update_cart_item'}), name='update-cart-item'),
    path('add_to_cart/<int:product_id>/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', CartViewSet.as_view({'post': 'remove_from_cart'}), name='remove_from_cart'),
    path('clear_cart/', CartViewSet.as_view({'delete': 'clear_cart'}), name='clear_cart'),
]
