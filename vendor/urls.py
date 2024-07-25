from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore 
from .views import VendorViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')


urlpatterns = [
    path('', include(router.urls)),
    path('delete_vendor/<int:pk>', VendorViewSet.as_view({'delete': 'delete_vendor'})),
]
