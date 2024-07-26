### Ratings App Documentation ###

## Overview ##
The Ratings app allows users to rate and review products. It includes two primary models: Rating and Review. This documentation outlines the fields, methods, and validations for each model, as well as the serializers and signal handlers.

## Models.py ##
================

### Rating Model

#### Fields

1. `user`
   - **Type**: ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
   - **Description**: Links the rating to a user. If the user is deleted, the rating will still exist but will be associated with null.
   - **Validation**: No additional validation; allows null and blank values.

2. `product`
   - **Type**: ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
   - **Description**: Associates the rating with a product. If the product is deleted, all related ratings will also be deleted.
   - **Validation**: No additional validation.

3. `rating`
   - **Type**: IntegerField(choices=[(i, i) for i in range(1, 6)])
   - **Description**: Stores the rating value from 1 to 5.
   - **Validation**: Must be an integer between 1 and 5.

4. `created_at`
   - **Type**: DateTimeField(auto_now_add=True)
   - **Description**: Timestamp of when the rating was created.
   - **Validation**: Automatically set when the rating is created.

5. `updated_at`
   - **Type**: DateTimeField(auto_now=True)
   - **Description**: Timestamp of when the rating was last updated.
   - **Validation**: Automatically updated on each save.

#### Methods

1. **__str__()**
   - **Description**: Returns a string representation of the rating.
   - **Implementation**: Displays the product name and the rating value.
   - **Returns**: A formatted string with the product name and rating value.

### Review Model

#### Fields

1. `user`
   - **Type**: ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
   - **Description**: Links the review to a user. If the user is deleted, the review will still exist but will be associated with null.
   - **Validation**: No additional validation; allows null and blank values.

2. `product`
   - **Type**: ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
   - **Description**: Associates the review with a product. If the product is deleted, all related reviews will also be deleted.
   - **Validation**: No additional validation.

3. `review`
   - **Type**: TextField()
   - **Description**: Contains the text of the review.
   - **Validation**: No additional validation.

4. `rating`
   - **Type**: ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True, related_name='review_rating')
   - **Description**: Links the review to a rating. If the rating is deleted, the review will still exist but will be associated with null.
   - **Validation**: Allows null and blank values.

5. `created_at`
   - **Type**: DateTimeField(auto_now_add=True)
   - **Description**: Timestamp of when the review was created.
   - **Validation**: Automatically set when the review is created.

6. `updated_at`
   - **Type**: DateTimeField(auto_now=True)
   - **Description**: Timestamp of when the review was last updated.
   - **Validation**: Automatically updated on each save.

#### Methods

1. **__str__()**
   - **Description**: Returns a string representation of the review.
   - **Implementation**: Displays the product name and the first 30 characters of the review.
   - **Returns**: A formatted string with the product name and a truncated review text.

---

## Serializers.py ##
====================

### RatingSerializer

#### Fields

1. `user`
   - **Type**: Read-only.
   - **Description**: The user who created the rating. Automatically populated based on the request.

2. `product`
   - **Type**: Read-only.
   - **Description**: The product associated with the rating. Automatically populated.

3. `rating`
   - **Type**: IntegerField.
   - **Description**: The rating value from 1 to 5.

4. `created_at`
   - **Type**: Read-only.
   - **Description**: Timestamp of when the rating was created.

5. `updated_at`
   - **Type**: Read-only.
   - **Description**: Timestamp of when the rating was last updated.

#### Validations

- **rating**: Must be an integer between 1 and 5.

### ReviewSerializer

#### Fields

1. `user`
   - **Type**: Read-only.
   - **Description**: The user who created the review. Automatically populated.

2. `product`
   - **Type**: Read-only.
   - **Description**: The product associated with the review. Automatically populated.

3. `review`
   - **Type**: TextField.
   - **Description**: The text content of the review.

4. `rating`
   - **Type**: Nested RatingSerializer (read-only).
   - **Description**: The associated rating details for the review.

5. `rating_id`
   - **Type**: PrimaryKeyRelatedField (write-only).
   - **Description**: The ID of the rating associated with the review.

6. `created_at`
   - **Type**: Read-only.
   - **Description**: Timestamp of when the review was created.

7. `updated_at`
   - **Type**: Read-only.
   - **Description**: Timestamp of when the review was last updated.

#### Validations

- **rating_id**: Must correspond to an existing rating.

---

## Signals.py ##
================

### Signal Handlers

#### update_product_rating_on_save

- **Signal**: post_save
- **Sender**: Rating
- **Description**: Updates the product's rating when a new rating is saved.
- **Implementation**: Calls the update_rating method on the product instance whenever a rating is saved.
- **Validation**: Ensures that product ratings are recalculated whenever a rating is added or updated.

#### update_product_rating_on_delete

- **Signal**: post_delete
- **Sender**: Rating
- **Description**: Updates the product's rating when a rating is deleted.
- **Implementation**: Calls the update_rating method on the product instance whenever a rating is deleted.
- **Validation**: Ensures that product ratings are recalculated whenever a rating is deleted.

---

### Product Model Considerations

The Product model, which is part of the products app, includes a rating field. It is crucial for the rating system to ensure consistency and accuracy of the product ratings.

**Field in Product Model:**

1. `rating`
   - **Type**: IntegerField (or other suitable type based on implementation).
   - **Description**: Represents the average rating of the product, calculated based on all associated ratings.
   - **Validation**: Should be updated based on the calculations done in the update_rating method whenever a rating is added, updated, or removed.

**Methods:**

1. **update_rating**
   - **Description**: Method in the Product model that recalculates the average rating based on the associated ratings.
   - **Implementation**: Calculates the average of all ratings linked to the product and updates the rating field accordingly.

---

## Views.py ##
================

### RatingListCreateView

**Endpoint:** GET /ratings/, POST /ratings/

**Description:** 
- **GET**: Lists all ratings.
- **POST**: Creates a new rating. 

**Permissions:** IsAuthenticatedOrReadOnly
- **Authenticated Users**: Can create ratings.
- **Unauthenticated Users**: Can view ratings.

**Validation and Error Handling:**
- **POST**: Ensures a user can only create one rating per product. If a rating already exists for the product by the user, a ValidationError is raised with the message: "You cannot create a second rating for the same product. Please update your existing rating."

**Methods:**
- **perform_create(self, serializer)**: Checks if the user has already rated the product. If so, raises a ValidationError. If not, saves the rating with the current user and returns a success message.

### RatingDetailView

**Endpoint:** GET /ratings/<int:pk>/, PUT /ratings/<int:pk>/, DELETE /ratings/<int:pk>/

**Description:** 
- **GET**: Retrieves a specific rating by its ID.
- **PUT**: Updates an existing rating by its ID.
- **DELETE**: Deletes an existing rating by its ID.

**Permissions:** IsAuthenticatedOrReadOnly
- **Authenticated Users**: Can update or delete their own ratings.
- **Unauthenticated Users**: Can view ratings.

**Validation and Error Handling:**
- **PUT**: Checks if the requesting user is the owner of the rating. If not, a 403 Forbidden response is returned with the message: "You can only update your own rating."
- **DELETE**: Checks if the requesting user is the owner of the rating. If not, a 403 Forbidden response is returned with the message: "You can only delete your own rating."

**Methods:**
- **update(self, request, **args, **kwargs)**: Checks ownership and updates the rating if valid. Adds a success message to the response.
- **destroy(self, request, **args, **kwargs)**: Checks ownership and deletes the rating if valid. Adds a success message to the response.

### ReviewListCreateView

**Endpoint:** GET /reviews/, POST /reviews/

**Description:**
- **GET**: Lists all reviews.
- **POST**: Creates a new review.

**Permissions:** IsAuthenticatedOrReadOnly
- **Authenticated Users**: Can create reviews.
- **Unauthenticated Users**: Can view reviews.

**Validation and Error Handling:**
- **POST**: Ensures a user can only create one review per product. If a review already exists for the product by the user, a ValidationError is raised with the message: "You cannot create a second review for the same product. Please update your existing review."
- **POST**: Ensures the provided rating exists and belongs to the user. If a rating is provided that does not belong to the user, a ValidationError is raised with the message: "Invalid rating. You can only use your own ratings."
- **POST**: If no rating is provided, checks if the user has already rated the product. If not, raises a ValidationError with the message: "You need to rate the product before writing a review."

**Methods:**
- **perform_create(self, serializer)**: Performs validation checks and creates the review if valid. Saves the review with the current user and associated rating, if any. Returns a success message.

### ReviewDetailView

**Endpoint:** GET /reviews/<int:pk>/, PUT /reviews/<int:pk>/, DELETE /reviews/<int:pk>/

**Description:**
- **GET**: Retrieves a specific review by its ID.
- **PUT**: Updates an existing review by its ID.
- **DELETE**: Deletes an existing review by its ID.

**Permissions:** IsAuthenticatedOrReadOnly
- **Authenticated Users**: Can update or delete their own reviews.
- **Unauthenticated Users**: Can view reviews.

**Validation and Error Handling:**
- **PUT**: Checks if the requesting user is the owner of the review. If not, a 403 Forbidden response is returned with the message: "You can only update your own review."
- **DELETE**: Checks if the requesting user is the owner of the review. If not, a 403 Forbidden response is returned with the message: "You can only delete your own review."

**Methods:**
- **update(self, request, **args, **kwargs)**: Checks ownership and updates the review if valid. Adds a success message to the response.
- **destroy(self, request, **args, **kwargs)**: Checks ownership and deletes the review if valid. Adds a success message to the response.

### ProductRatingsAndReviewsView

**Endpoint:** GET /products/<int:product_id>/ratings-reviews/

**Description:**
- Retrieves ratings and reviews for a specific product.
- Also calculates the distribution of ratings.

**Permissions:** IsAuthenticatedOrReadOnly
- **Authenticated Users**: Can view ratings and reviews.
- **Unauthenticated Users**: Can view ratings and reviews.

**Validation and Error Handling:**
- **GET**: Checks if the product exists. If not, raises a ValidationError with the message: "Product not found."

**Methods:**
- **get_queryset(self)**: Retrieves reviews for the specified product. Raises a ValidationError if the product does not exist.
- **list(self, request, **args, **kwargs)**: Retrieves and serializes reviews and ratings for the product. Calculates the distribution of ratings and ensures all ratings from 1 to 5 are represented, even if the count is 0. Returns a comprehensive response with ratings, reviews, and rating distribution.

---

## URLs.py ##
================

### URL Patterns

1. **RatingListCreateView**
   - **Path:** ratings/
   - **Methods:** GET, POST
   - **View:** RatingListCreateView
   - **Description:** Lists all ratings and creates a new rating.

2. **RatingDetailView**
   - **Path:** ratings/<int:pk>/
   - **Methods:** GET, PUT, DELETE
   - **View:** RatingDetailView
   - **Description:** Retrieves, updates, or deletes a specific rating.

3. **ReviewListCreateView**
   - **Path:** reviews/
   - **Methods:** GET, POST
   - **View:** ReviewListCreateView
   - **Description:** Lists all reviews and creates a new review.

4. **ReviewDetailView**
   - **Path:** reviews/<int:pk>/
   - **Methods:** GET, PUT, DELETE
   - **View:** ReviewDetailView
   - **Description:** Retrieves, updates, or deletes a specific review.

5. **ProductRatingsAndReviewsView**
   - **Path:** products/<int:product_id>/ratings-reviews/
   - **Methods:** GET
   - **View:** ProductRatingsAndReviewsView
   - **Description:** Retrieves ratings and reviews for a specific product and calculates rating distribution.

---
