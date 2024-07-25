from rest_framework import generics, permissions
from .models import Wishlist, WishlistItem
from rest_framework.exceptions import ValidationError
from .serializers import WishlistSerializer, WishlistItemSerializer


class WishlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure the user does not already have a wishlist
        if Wishlist.objects.filter(user=self.request.user).exists():
            raise ValidationError("You already have a wishlist.")
        serializer.save(user=self.request.user)


class WishlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class WishlistItemListCreateView(generics.ListCreateAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure that the wishlist belongs to the authenticated user
        return WishlistItem.objects.filter(
            wishlist__user=self.request.user,
            wishlist_id=self.kwargs['wishlist_id']
        )

    def perform_create(self, serializer):
        wishlist_id = self.kwargs['wishlist_id']
        # Ensure that the wishlist belongs to the authenticated user
        if not Wishlist.objects.filter(id=wishlist_id, user=self.request.user).exists():
            raise ValidationError("Invalid wishlist ID.")
        serializer.save(wishlist_id=wishlist_id)


class WishlistItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(wishlist__user=self.request.user)
