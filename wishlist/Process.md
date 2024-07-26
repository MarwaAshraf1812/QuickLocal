# **Wishlist App Process Documentation**

## **User Experience Overview**

The Wishlist app allows users to manage their wishlists and add items to them. It includes functionalities for creating, viewing, updating, and deleting wishlists and items within them. Below is a detailed user story flow for each process, incorporating endpoints, interactions with various components, validations, and messages.

## User Story and Process Flow ##

### 1. Wishlist Creation ###

`Endpoint:` POST /wishlists/

`User Story:`
- Authenticated users can create a new wishlist.
- Users cannot create more than one wishlist. If they try, an error is returned.

`Process:`
1. **Request Handling:**
   - User submits a request to the /wishlists/ endpoint to create a new wishlist.
   - **View:** WishlistListCreateView in views.py.
   - **Serializer:** WishlistSerializer validates and processes the data.

2. **Validation:**
   - **Existing Wishlist Check:** Users cannot create more than one wishlist.
     - **Error Message:** "You already have an existing wishlist."

3. **Wishlist Creation:**
   - A new wishlist is created for the user if validation passes.
   - **Response:** Returns a success message upon successful creation.
     - **Success Message:** "Wishlist created successfully."

### 2. View Wishlist ###

`Endpoint:` GET /wishlists/<int:pk>/

`User Story:`
- Authenticated users can view their own wishlist.

`Process:`
1. **Request Handling:**
   - User requests to view their wishlist via /wishlists/<pk>/.
   - **View:** WishlistDetailView in views.py.

2. **Data Retrieval:**
   - Retrieves the wishlist associated with the user.

3. **Response:**
   - Returns the wishlist details.
   - **Error Handling:** If the wishlist does not belong to the user, return an appropriate message.
     - **Error Message:** "Wishlist not found."

### 3. Update Wishlist ###

`Endpoint:` PUT /wishlists/<int:pk>/

`User Story:`
- Users can update their existing wishlist.
- Only the user who created the wishlist can update it.

`Process:`
1. **Request Handling:**
   - User submits updated wishlist details to /wishlists/<pk>/.
   - **View:** WishlistDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who created the wishlist can update it.
     - **Error Message:** "You can only update your own wishlist."

3. **Wishlist Update:**
   - Updates the wishlist if the user is authorized.
   - **Response:** Returns a success message upon successful update.
     - **Success Message:** "Wishlist updated successfully."

### 4. Delete Wishlist ###

`Endpoint:` DELETE /wishlists/<int:pk>/

`User Story:`
- Users can delete their own wishlist.
- Only the user who created the wishlist can delete it.

`Process:`
1. **Request Handling:**
   - User requests to delete a wishlist via /wishlists/<pk>/.
   - **View:** WishlistDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who created the wishlist can delete it.
     - **Error Message:** "You can only delete your own wishlist."

3. **Wishlist Deletion:**
   - Deletes the wishlist if the user is authorized.
   - **Response:** Returns a success message upon successful deletion.
     - **Success Message:** "Wishlist deleted successfully."

### 5. Add Item to Wishlist ###

`Endpoint:` POST /wishlists/<int:wishlist_id>/items/

`User Story:`
- Authenticated users can add items to their wishlist.
- Users can only add items to their own wishlist.

`Process:`
1. **Request Handling:**
   - User submits a request to add an item to their wishlist via /wishlists/<wishlist_id>/items/.
   - **View:** WishlistItemListCreateView in views.py.
   - **Serializer:** WishlistItemSerializer validates and processes the data.

2. **Validation:**
   - **Wishlist Ownership Check:** Users can only add items to their own wishlist.
     - **Error Message:** "You can only add items to your own wishlist."
   - **Item Validation:** Ensure the item exists and is valid.

3. **Item Addition:**
   - Adds the item to the specified wishlist if validation passes.
   - **Response:** Returns a success message upon successful addition.
     - **Success Message:** "Item added to wishlist successfully."

### 6. View Items in Wishlist ###

`Endpoint:` GET /wishlists/<int:wishlist_id>/items/

`User Story:`
- Authenticated users can view all items in their own wishlist.

`Process:`
1. **Request Handling:**
   - User requests to view items in their wishlist via /wishlists/<wishlist_id>/items/.
   - **View:** WishlistItemListView in views.py.

2. **Data Retrieval:**
   - Retrieves all items associated with the specified wishlist.

3. **Response:**
   - Returns the list of items in the wishlist.
   - **Error Handling:** If the wishlist does not belong to the user, return an appropriate message.
     - **Error Message:** "Wishlist not found."

### 7. Update Wishlist Item ###

`Endpoint:` PUT /wishlists/items/<int:pk>/

`User Story:`
- Users can update items in their wishlist.
- Only the user who owns the wishlist can update its items.

`Process:`
1. **Request Handling:**
   - User submits updated item details to /wishlists/items/<pk>/.
   - **View:** WishlistItemDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who owns the wishlist can update items.
     - **Error Message:** "You can only update items in your own wishlist."

3. **Item Update:**
   - Updates the item if the user is authorized.
   - **Response:** Returns a success message upon successful update.
     - **Success Message:** "Wishlist item updated successfully."

### 8. Delete Wishlist Item ###

`Endpoint:` DELETE /wishlists/items/<int:pk>/

`User Story:`
- Users can delete items from their wishlist.
- Only the user who owns the wishlist can delete its items.

`Process:`
1. **Request Handling:**
   - User requests to delete an item from their wishlist via /wishlists/items/<pk>/.
   - **View:** WishlistItemDetailView in views.py.

2. **Validation:**
   - **Ownership Check:** Only the user who owns the wishlist can delete items.
     - **Error Message:** "You can only delete items from your own wishlist."

3. **Item Deletion:**
   - Deletes the item if the user is authorized.
   - **Response:** Returns a success message upon successful deletion.
     - **Success Message:** "Wishlist item deleted successfully."


## Endpoints Summary ##

1. **WishlistListCreateView**
   - **POST /wishlists/** - Create a new wishlist.

2. **WishlistDetailView**
   - **GET /wishlists/<int:pk>/** - View details of a wishlist.
   - **PUT /wishlists/<int:pk>/** - Update an existing wishlist.
   - **DELETE /wishlists/<int:pk>/** - Delete an existing wishlist.

3. **WishlistItemListCreateView**
   - **POST /wishlists/<int:wishlist_id>/items/** - Add a new item to a wishlist.

4. **WishlistItemListView**
   - **GET /wishlists/<int:wishlist_id>/items/** - View all items in a wishlist.

5. **WishlistItemDetailView**
   - **PUT /wishlists/items/<int:pk>/** - Update an existing wishlist item.
   - **DELETE /wishlists/items/<int:pk>/** - Delete an existing wishlist item.

---
