### Orders App Documentation

#### Overview
This app handles order management, including creating orders from cart items, retrieving user-specific orders, and managing order details using Django and Django REST Framework.

### Components

#### Models

1. **Order**
   - Represents an order made by a user.
   - Fields: `user`, `total_amount`, `created_at`, `updated_at`.

2. **OrderItem**
   - Represents an item within an order.
   - Fields: `order`, `product`, `quantity`, `price`.

#### Serializers

- **OrderSerializer**
  - Serializes the `Order` model.
  - Fields: `user`, `total_amount`, `created_at`, `updated_at`, `items`.

- **CreateOrderSerializer**
  - Validates data for creating an order.
  - Fields: `user`, `total_amount`, `items`, `stripe_token`.

- **UpdateOrderSerializer**
  - Validates data for updating an order.
  - Fields: `total_amount`.

#### Views

- **OrderViewSet**
  - Manages order operations.
  - Requires authentication.
  - Endpoints:
    - `POST /create_order/`: Create a new order from cart items.
    - `GET /user_orders/`: Retrieve all orders for the authenticated user.
    - `GET /order_detail/(?P<pk>[^/.]+)`: Retrieve a specific order by its ID.
    - `GET /list_all_orders/`: Retrieve all orders (Admin only).
    - `PUT /update_order/(?P<pk>[^/.]+)`: Update an existing order.
    - `DELETE /delete_order/(?P<pk>[^/.]+)`: Delete an order by its ID.

### Process

1. **Create Order**
   - Endpoint: `POST /create_order/`
   - Request Data: `{"items": [{"product": 1, "quantity": 2, "price": 100}], "stripe_token": "tok_visa"}`

2. **Retrieve User Orders**
   - Endpoint: `GET /user_orders/`

3. **Retrieve Order Details**
   - Endpoint: `GET /order_detail/(?P<pk>[^/.]+)`

4. **List All Orders (Admin Only)**
   - Endpoint: `GET /list_all_orders/`

5. **Update Order**
   - Endpoint: `PUT /update_order/(?P<pk>[^/.]+)`
   - Request Data: `{"total_amount": 200}`

6. **Delete Order**
   - Endpoint: `DELETE /delete_order/(?P<pk>[^/.]+)`