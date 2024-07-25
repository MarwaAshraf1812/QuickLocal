from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Rating, Review
from .serializers import RatingSerializer, ReviewSerializer
from products.models import Product
from django.db.models import Count


class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Check if the user has already rated this product
        product = serializer.validated_data['product']
        if Rating.objects.filter(user=self.request.user, product=product).exists():
            raise ValidationError('You cannot create a second rating for the same product. Please update your existing rating.')
        serializer.save(user=self.request.user)
        return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'You can only update your own rating.'}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Rating updated successfully'
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'You can only delete your own rating.'}, status=status.HTTP_403_FORBIDDEN)
        response = super().destroy(request, *args, **kwargs)
        response.data = {'message': 'Rating deleted successfully'}
        return response


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        rating = serializer.validated_data.get('rating')

        # Check if the user has already created a review for this product
        if Review.objects.filter(user=user, product=product).exists():
            raise ValidationError('You cannot create a second review for the same product. Please update your existing review.')

        # Ensure the rating exists and belongs to the user
        if rating and rating.user != user:
            raise ValidationError('Invalid rating. You can only use your own ratings.')

        # If no rating is provided, check if the user has already rated the product
        if not rating:
            rating = Rating.objects.filter(user=user, product=product).first()
            if not rating:
                raise ValidationError('You need to rate the product before writing a review.')

        serializer.save(user=user, rating=rating)
        return Response({'message': 'Review added successfully'}, status=status.HTTP_201_CREATED)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'You can only update your own review.'}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Review updated successfully'
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'You can only delete your own review.'}, status=status.HTTP_403_FORBIDDEN)
        response = super().destroy(request, *args, **kwargs)
        response.data = {'message': 'Review deleted successfully'}
        return response
    
class ProductRatingsAndReviewsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product not found.')
        return Review.objects.filter(product=product)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        reviews_serializer = self.get_serializer(queryset, many=True)
        
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        
        ratings = Rating.objects.filter(product=product)
        ratings_serializer = RatingSerializer(ratings, many=True)
        
        # Calculate rating distribution
        rating_distribution = ratings.values('rating').annotate(count=Count('rating')).order_by('rating')
        
        # Create a dictionary with rating distribution
        rating_dist_dict = {str(item['rating']): item['count'] for item in rating_distribution}
        
        # Ensure all ratings from 1 to 5 are represented, even if count is 0
        for i in range(1, 6):
            if str(i) not in rating_dist_dict:
                rating_dist_dict[str(i)] = 0
        
        return Response({
            'ratings': ratings_serializer.data,
            'reviews': reviews_serializer.data,
            'rating_distribution': rating_dist_dict,
        }, status=status.HTTP_200_OK)
        
        
