from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore
from cart.views import CartViewSet

app_name = 'cart'

router = DefaultRouter()
router.register(r'cart', CartViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('addToCart/<int:product_id>/', CartViewSet.as_view({'post': 'addToCart'}), name='addToCart'),
    path('removeFromCart/<int:product_id>/', CartViewSet.as_view({'post': 'removeFromCart'}), name='removeFromCart'),
    path('cartDetails/', CartViewSet.as_view({'get': 'cartDetails'}), name='cartDetails'),
]