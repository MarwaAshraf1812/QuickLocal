from django.urls import path
from .views import (
    WishlistListCreateView, WishlistDetailView,
    WishlistItemListCreateView, WishlistItemDetailView
)

urlpatterns = [
    path('wishlists/', WishlistListCreateView.as_view(), name='wishlist-list-create'),
    path('wishlists/<int:pk>/', WishlistDetailView.as_view(), name='wishlist-detail'),
    path('wishlists/<int:wishlist_id>/items/', WishlistItemListCreateView.as_view(), name='wishlistitem-list-create'),
    path('wishlists/items/<int:pk>/', WishlistItemDetailView.as_view(), name='wishlistitem-detail'),
]
