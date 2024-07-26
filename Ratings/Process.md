# **Ratings and Reviews App Process Documentation**

## **User Experience Overview**

The Ratings and Reviews App allows users to rate and review products within the e-commerce platform. It includes functionalities for submitting ratings and reviews, viewing ratings and reviews for products, and managing individual ratings and reviews. Below is a detailed user story flow for each process, incorporating endpoints, interactions with various components, validations, and messages.

## User Story and Process Flow ##

## 1. Rating Submission ##

`Endpoint:` POST /ratings/

`User Story:`
- Authenticated users can submit a rating for a product.
- Users cannot rate a product more than once. If they try, an error is returned.

`Process:`
1. **Request Handling:**
   - User submits a rating to the /ratings/ endpoint.
   - **View:** RatingListCreateView in views.py.
   - **Serializer:** RatingSerializer validates and processes the data.

2. **Validation:**
   - **Rating Value Check:** Rating value must be between 1 and 5.
     - **Error Message:** "Rating must be between 1 and 5."
   - **Unique Rating Check:** Users cannot submit more than one rating for the same product.
     - **Error Message:** "You have already rated this product."

3. **Rating Creation:**
   - A new rating is created for the product if validation passes.
   - **Response:** Returns a success message upon successful creation.
     - **Success Message:** "Rating submitted successfully."


## 2. Rating Update ##

`Endpoint:` PUT /ratings/<int:pk>/

`User Story:`
- Users can update their existing rating for a product.
- Only the user who submitted the rating can update it.

``Process:``
1. **Request Handling:**
   - User submits updated rating details to /ratings/<pk>/.
   - **View:** RatingDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who submitted the rating can update it.
     - **Error Message:** "You can only update your own rating."
   - **Rating Value Check:** Rating value must be between 1 and 5.
     - **Error Message:** "Rating must be between 1 and 5."

3. **Rating Update:**
   - Updates the rating if the user is authorized.
   - **Response:** Returns a success message upon successful update.
     - **Success Message:** "Rating updated successfully."


## 3. Rating Deletion ##

`Endpoint:` DELETE /ratings/<int:pk>/

`User Story:`
- Users can delete their own ratings.
- Only the user who submitted the rating can delete it.

`Process:`
1. **Request Handling:**
   - User requests to delete a rating via /ratings/<pk>/.
   - **View:** RatingDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who submitted the rating can delete it.
     - **Error Message:** "You can only delete your own rating."

3. **Rating Deletion:**
   - Deletes the rating if the user is authorized.
   - **Response:** Returns a success message upon successful deletion.
     - **Success Message:** "Rating deleted successfully."


## 4. Review Submission ##

`Endpoint:` POST /reviews/

`User Story:`
- Authenticated users can submit a review for a product.
- Users must either provide a rating or have previously rated the product.

`Process:`
1. **Request Handling:**
   - User submits a review to the /reviews/ endpoint.
   - **View:** ReviewListCreateView in views.py.
   - **Serializer:** ReviewSerializer validates and processes the data.

2. **Validation:**
   - **Rating Requirement:** Users must provide a rating or have an existing rating for the product.
     - **Error Message:** "You must provide a rating or have previously rated this product."
   - **Review Length Check:** Review text must not exceed 1000 characters.
     - **Error Message:** "Review text must not exceed 1000 characters."

3. **Review Creation:**
   - A new review is created if validation passes.
   - **Response:** Returns a success message upon successful creation.
     - **Success Message:** "Review submitted successfully."

## 5. Review Update ##

`Endpoint:` PUT /reviews/<int:pk>/

`User Story:`
- Users can update their existing review.
- Only the user who submitted the review can update it.

`Process:`
1. **Request Handling:**
   - User submits updated review details to /reviews/<pk>/.
   - **View:** ReviewDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who submitted the review can update it.
     - **Error Message:** "You can only update your own review."
   - **Review Length Check:** Updated review text must not exceed 1000 characters.
     - **Error Message:** "Review text must not exceed 1000 characters."

3. **Review Update:**
   - Updates the review if the user is authorized.
   - **Response:** Returns a success message upon successful update.
     - **Success Message:** "Review updated successfully."


## 6. Review Deletion ##

`Endpoint:` DELETE /reviews/<int:pk>/

`User Story:`
- Users can delete their own reviews.
- Only the user who submitted the review can delete it.

`Process:`
1. **Request Handling:**
   - User requests to delete a review via /reviews/<pk>/.
   - **View:** ReviewDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who submitted the review can delete it.
     - **Error Message:** "You can only delete your own review."

3. **Review Deletion:**
   - Deletes the review if the user is authorized.
   - **Response:** Returns a success message upon successful deletion.
     - **Success Message:** "Review deleted successfully."


## 7. Product Ratings and Reviews Overview ##

`Endpoint:` GET /products/<int:product_id>/ratings-reviews/

`User Story:`
- Users can view all ratings and reviews for a specific product.
- The response includes rating distribution and reviews for the product.

`Process:`
1. **Request Handling:**
   - User requests ratings and reviews for a product via /products/<product_id>/ratings-reviews/.
   - **View:** ProductRatingsAndReviewsView in views.py.

2. **Data Retrieval:**
   - Retrieves all reviews and ratings for the product.
   - Calculates the distribution of ratings (1 to 5).

3. **Response:**
   - Returns the list of ratings and reviews along with the rating distribution.
   - **Error Handling:** If no ratings or reviews are found, returns an appropriate message.
     - **Error Message:** "No ratings or reviews found for this product."

## Custom Signals ##

**1. Signals**

**File:** signals.py

- **Signal:** create_or_update_review(sender, instance, created, ****kwargs) ensures that a review's rating is validated when created or updated.
- **Signal:** create_or_update_rating(sender, instance, created, ****kwargs) ensures that the rating is updated or created appropriately.

## Endpoints Summary ##

1. **RatingListCreateView**
   - **POST /ratings/** - Submit a new rating.

2. **RatingDetailView**
   - **PUT /ratings/<int:pk>/** - Update an existing rating.
   - **DELETE /ratings/<int:pk>/** - Delete an existing rating.

3. **ReviewListCreateView**
   - **POST /reviews/** - Submit a new review.

4. **ReviewDetailView**
   - **PUT /reviews/<int:pk>/** - Update an existing review.
   - **DELETE /reviews/<int:pk>/** - Delete an existing review.

5. **ProductRatingsAndReviewsView**
   - **GET /products/<int:product_id>/ratings-reviews/** - View ratings and reviews for a specific product.
