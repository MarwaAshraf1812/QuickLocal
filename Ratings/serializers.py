from rest_framework import serializers
from .models import Rating, Review


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)  # Nested serializer for read-only
    rating_id = serializers.PrimaryKeyRelatedField(queryset=Rating.objects.all(), source='rating', write_only=True)  # For creating a review with rating

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
