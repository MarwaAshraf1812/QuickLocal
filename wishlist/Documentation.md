## Wishlist App Documentation ##

## **Overview**

The Wishlist app enables users to create and manage their personal wishlists. Each wishlist can contain multiple products. The app provides functionality for users to add items to their wishlists, view their wishlists, and remove items as needed. This documentation details the models, serializers, and key functionality of the Wishlist app.


## Models.py ##
================

#### **Wishlist Model**

`Fields:`

1. **user**
   - Type: ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
   - Description: Links the wishlist to a user. If the user is deleted, all associated wishlists will also be deleted.
   - Validation: No additional validation.

2. **created_at**
   - Type: DateTimeField(auto_now_add=True)
   - Description: Timestamp when the wishlist was created.
   - Validation: Automatically set when the wishlist is created.

3. **updated_at**
   - Type: DateTimeField(auto_now=True)
   - Description: Timestamp when the wishlist was last updated.
   - Validation: Automatically updated on each save.

`Methods:`

1. **_str_()**
   - Description: Returns a string representation of the wishlist.
   - Implementation: Displays the username associated with the wishlist.
   - Returns: A formatted string indicating the wishlist owner.

#### **WishlistItem Model**

`Fields:`

1. **wishlist**
   - Type: ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
   - Description: Links the item to a wishlist. If the wishlist is deleted, all associated items will also be deleted.
   - Validation: No additional validation.

2. **product**
   - Type: ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
   - Description: Associates the item with a product. If the product is deleted, all associated wishlist items will also be deleted.
   - Validation: No additional validation.

3. **added_at**
   - Type: DateTimeField(auto_now_add=True)
   - Description: Timestamp when the item was added to the wishlist.
   - Validation: Automatically set when the item is added.

`Methods:`

1. **_str_()**
   - Description: Returns a string representation of the wishlist item.
   - Implementation: Displays the product name and the associated wishlist.
   - Returns: A formatted string with the product name and wishlist.

---

## Serializers.py ##
====================

#### **WishlistSerializer**

`Fields:`

1. **user**
   - Type: Read-only.
   - Description: The user who owns the wishlist. Automatically populated based on the request.

2. **created_at**
   - Type: Read-only.
   - Description: Timestamp when the wishlist was created.

3. **updated_at**
   - Type: Read-only.
   - Description: Timestamp when the wishlist was last updated.

`Validations:`

- Wishlist: Ensures that each user has only one wishlist.
   - Validation Logic: Checks if a wishlist already exists for the user; raises a validation error if a new wishlist is being created for a user who already has one.

#### **WishlistItemSerializer**

`Fields:`

1. **wishlist**
   - Type: Read-only.
   - Description: The wishlist to which the item belongs. Automatically populated.

2. **product**
   - Type: Read-only.
   - Description: The product associated with the wishlist item. Automatically populated.

3. **added_at**
   - Type: Read-only.
   - Description: Timestamp when the item was added to the wishlist.

---


## Views.py ##
===============

### WishlistListCreateView

`Endpoint:`
- **GET** /wishlists/
- **POST** /wishlists/

`Description:` 
- **GET**: Lists all wishlists belonging to the authenticated user.
- **POST**: Creates a new wishlist for the authenticated user. Only one wishlist per user is allowed.

`Permissions:` 
- **Authenticated Users**: Can create and view their own wishlists.
- **Unauthenticated Users**: Cannot access this endpoint.

`Validation and Error Handling:`
- **POST**: Ensures that the user does not already have a wishlist. If a wishlist already exists, a ValidationError is raised with the message: "You already have a wishlist."

`Methods:`
- **perform_create(self, serializer)**: Checks if a wishlist already exists for the user. If it does, a ValidationError is raised. If not, it saves the new wishlist with the current user and returns a success message.

### WishlistDetailView

`Endpoint:`
- **GET** /wishlists/<int:pk>/
- **PUT** /wishlists/<int:pk>/
- **DELETE** /wishlists/<int:pk>/

`Description:` 
- **GET**: Retrieves details of a specific wishlist by its ID.
- **PUT**: Updates an existing wishlist by its ID.
- **DELETE**: Deletes an existing wishlist by its ID.

`Permissions:` 
- **Authenticated Users**: Can update or delete their own wishlists.
- **Unauthenticated Users**: Cannot access this endpoint.

`Validation and Error Handling:`
- **PUT**: Checks if the requesting user is the owner of the wishlist. If not, a 403 Forbidden response is returned with the message: "You cannot modify someone else's wishlist."
- **DELETE**: Checks if the requesting user is the owner of the wishlist. If not, a 403 Forbidden response is returned with the message: "You cannot delete someone else's wishlist."

`Methods:`
- **update(self, request, ****args, ****kwargs)**: Checks ownership and updates the wishlist if valid. Returns a success message.
- **destroy(self, request, ****args, ****kwargs)**: Checks ownership and deletes the wishlist if valid. Returns a success message.

### WishlistItemListCreateView

`Endpoint:`
- **GET** /wishlists/<int:wishlist_id>/items/
- **POST** /wishlists/<int:wishlist_id>/items/

`Description:` 
- **GET**: Lists all items in a specific wishlist belonging to the authenticated user.
- **POST**: Adds a new item to a specific wishlist.

`Permissions:` 
- **Authenticated Users**: Can add items to and view items in their own wishlists.
- **Unauthenticated Users**: Cannot access this endpoint.

`Validation and Error Handling:`
- **POST**: Ensures the wishlist ID provided belongs to the authenticated user. If not, a ValidationError is raised with the message: "Invalid wishlist ID."

`Methods:`
- **perform_create(self, serializer)**: Checks if the provided wishlist ID belongs to the authenticated user. If valid, it saves the new item to the wishlist and returns a success message.

### WishlistItemDetailView

`Endpoint:`
- **GET** /wishlists/items/<int:pk>/
- **PUT** /wishlists/items/<int:pk>/
- **DELETE** /wishlists/items/<int:pk>/

`Description:` 
- **GET**: Retrieves details of a specific item in a wishlist.
- **PUT**: Updates an existing item in a wishlist.
- **DELETE**: Deletes an item from a wishlist.

`Permissions:` 
- **Authenticated Users**: Can update or delete their own wishlist items.
- **Unauthenticated Users**: Cannot access this endpoint.

`Validation and Error Handling:`
- **PUT**: Checks if the wishlist to which the item belongs is owned by the requesting user. If not, a 403 Forbidden response is returned with the message: "You cannot modify items in someone else's wishlist."
- **DELETE**: Checks if the wishlist to which the item belongs is owned by the requesting user. If not, a 403 Forbidden response is returned with the message: "You cannot delete items from someone else's wishlist."

`Methods:`
- **update(self, request, ****args, ****kwargs)**: Checks ownership and updates the wishlist item if valid. Returns a success message.
- **destroy(self, request, ****args, ****kwargs)**: Checks ownership and deletes the wishlist item if valid. Returns a success message.

--- 
