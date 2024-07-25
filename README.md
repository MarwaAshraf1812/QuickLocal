# QuickLocal

QuickLocal is an advanced e-commerce platform designed to deliver a seamless online shopping experience. The system is built using Django and Django REST Framework, providing a robust backend to support various e-commerce functionalities, including product management, cart operations, order processing, vendor management, and user accounts.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [API Endpoints](#api-endpoints)
   - [Account Endpoints](#account-endpoints)
   - [Product Endpoints](#product-endpoints)
   - [Cart Endpoints](#cart-endpoints)
   - [Order Endpoints](#order-endpoints)
   - [Vendor Endpoints](#vendor-endpoints)
   - [Wishlist Endpoints](#wishlist-endpoints)
4. [Error Handling](#error-handling)
5. [Testing](#testing)
6. [Installation](#installation)
7. [Contributing](#contributing)
8. [License](#license)

## 1. Introduction

QuickLocal is designed to manage and streamline various aspects of an e-commerce website. It facilitates product browsing, cart management, order placement, and user account management. Additionally, it allows vendors to manage their product listings and administrators to oversee order processing and user management.

## 2. Features

- **Product Management**: Enables vendors to create, update, and delete products. Users can view products by category and search for specific items.
- **Cart Functionality**: Users can add items to their cart, view cart contents, and proceed to checkout.
- **Order Processing**: Users can place orders, with status updates handled automatically based on payment confirmation.
- **Vendor Management**: Vendors can manage their products and view their orders.
- **Wishlist**: Users can add items to their wishlist for future reference.
- **User Accounts**: Users can register, log in, and manage their account details.

## 3. API Endpoints

### Account Endpoints

- **Register**: `POST /register/` - Create a new user account.
- **Login**: `POST /login/` - Authenticate a user and return a token.
- **User Profile**: `GET /profile/` - Retrieve the details of the logged-in user.
- **Update Profile**: `PUT /profile/` - Update user details.

### Product Endpoints

- **List Products**: `GET /products/` - Retrieve a list of all products.
- **Retrieve Product**: `GET /products/{id}/` - Get details of a specific product.
- **Create Product**: `POST /products/` - Add a new product (Vendor only).
- **Update Product**: `PUT /products/{id}/` - Modify an existing product (Vendor only).
- **Delete Product**: `DELETE /products/{id}/` - Remove a product (Vendor only).

### Cart Endpoints

- **Add to Cart**: `POST /add-to-cart/{product_id}/` - Add a product to the cart.
- **View Cart**: `GET /list-cart-items/` - List all items in the cart.
- **Remove from Cart**: `POST /remove-from-cart/{product_id}/` - Remove a product from the cart.
- **Update Cart Item**: `POST /update-cart-item/{product_id}/` - Update product quantity in the cart.
- **Clear Cart**: `DELETE /clear-cart/` - Clear all items from the cart.

### Order Endpoints

- **Create Order**: `POST /create_order/` - Create a new order from cart items.
- **User Orders**: `GET /user_orders/` - Retrieve all orders for the authenticated user.
- **Order Detail**: `GET /order_detail/{pk}/` - Retrieve a specific order by its ID.
- **List All Orders**: `GET /list_all_orders/` - Retrieve all orders (Admin only).
- **Update Order**: `PUT /update_order/{pk}/` - Update an existing order.
- **Delete Order**: `DELETE /delete_order/{pk}/` - Delete an order by its ID.

### Vendor Endpoints

- **List Vendors**: `GET /vendors/` - Retrieve a list of all vendors.
- **Retrieve Vendor**: `GET /vendors/{id}/` - Get details of a specific vendor.
- **Create Vendor**: `POST /vendors/Create_vendor/` - Add a new vendor (Admin only).
- **Update Vendor**: `PUT /vendors/{id}/` - Modify a vendor's details (Admin only).
- **Delete Vendor**: `DELETE /vendors/{id}/` - Remove a vendor (Admin only).

### Wishlist Endpoints

- **View Wishlist**: `GET /wishlist/` - Retrieve items in the user's wishlist.
- **Add to Wishlist**: `POST /wishlist/add/` - Add an item to the wishlist.
- **Remove from Wishlist**: `DELETE /wishlist/remove/` - Remove an item from the wishlist.

## 4. Error Handling

QuickLocal utilizes Django REST Framework's built-in exception handling and custom error responses for specific scenarios:

- **Validation Errors**: Returned when required fields are missing or invalid data is provided.
- **Not Found Errors**: Returned when requested resources are not found.
- **Permission Errors**: Returned if the user lacks the necessary permissions to perform an action.
- **Internal Server Errors**: Returned for unexpected errors during processing.

## 5. Testing

To test the API endpoints, use tools like Postman . Below is an example of how to test the `create_order` endpoint:

### Example Request for `create_order`

**Endpoint**: `POST /create_order/`

**Request Body**:
```json
{
    "first_name": "Marwa",
    "last_name": "Ashraf",
    "email": "marashraf090@gmail.com",
    "address": "123 Main St",
    "postal_code": "12345",
    "city": "Anytown",
    "stripe_token": "pm_card_visa"
}
```

**Response**:
```json
{
    "order": {
        "id": 12,
        "first_name": "Marwa",
        "last_name": "Ashraf",
        "email": "marashraf090@gmail.com",
        "address": "123 Main St",
        "postal_code": "12345",
        "city": "Anytown",
        "total_amount": "29.99",
        "total_items": 1
    },
    "total_amount": "29.99",
    "total_items": 1,
    "order_items": [
        {
            "product": 9,
            "quantity": 1,
            "price": 29.99
        }
    ],
    "client_secret": "pi_1234567890_secret_abcdefghijk"
}
```

## 6. Installation

To set up the QuickLocal project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/QuickLocal.git
   ```
2. Navigate to the project directory:
   ```bash
   cd QuickLocal
   ```
3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## 7. Contributing

Contributions to QuickLocal are welcome. To contribute:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a pull request on GitHub.
