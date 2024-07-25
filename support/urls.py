from django.urls import path, include
from rest_framework.routers import DefaultRouter #type: ignore
from .views import SupportMessageViewSet

router = DefaultRouter()
router.register(r'support', SupportMessageViewSet, basename='support')

urlpatterns = [
    path('', include(router.urls)),
]