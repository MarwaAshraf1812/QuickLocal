from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore
from .views import OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
