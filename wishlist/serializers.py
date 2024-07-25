from rest_framework import serializers
from .models import Wishlist, WishlistItem

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['user']
        
def validate(self, data):
        user = self.context['request'].user
        if self.instance is None and Wishlist.objects.filter(user=user).exists():
            raise serializers.ValidationError("You already have a wishlist.")
        return data

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'
