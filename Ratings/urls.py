from django.urls import path
from .views import RatingListCreateView, RatingDetailView, ReviewListCreateView, ReviewDetailView, ProductRatingsAndReviewsView

urlpatterns = [
    path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('products/<int:product_id>/ratings-reviews/', ProductRatingsAndReviewsView.as_view(), name='product-ratings-reviews'),
]
