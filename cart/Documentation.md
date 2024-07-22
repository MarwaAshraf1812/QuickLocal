### Cart Management System Documentation

#### Overview
This system manages shopping cart operations such as adding, listing, updating, and removing items using Django and Django REST Framework.

### Components

#### Models

1. **Cart**
   - Represents the user's shopping cart.
   - Fields: `user`, `created_at`, `updated_at`.

2. **CartItem**
   - Represents an item in the cart.
   - Fields: `cart`, `product`, `quantity`, `price`.

#### Serializers

- **CartItemSerializer**
  - Serializes the `CartItem` model.
  - Fields: `product`, `quantity`, `price`.

#### Views

- **CartViewSet**
  - Manages cart operations.
  - Requires authentication.
  - Endpoints:
    - `POST /add-to-cart/(?P<product_id>[^/.]+)`: Add a product to the cart.
    - `GET /list-cart-items/`: List all items in the cart.
    - `POST /remove-from-cart/(?P<product_id>[^/.]+)`: Remove a product from the cart.
    - `POST /update-cart-item/(?P<product_id>[^/.]+)`: Update product quantity in the cart.
    - `DELETE /clear-cart/`: Clear all items from the cart.

### Process

1. **Add Product to Cart**
   - Endpoint: `POST /add-to-cart/(?P<product_id>[^/.]+)`
   - Request Data: `{"quantity": 2}`

2. **List Cart Items**
   - Endpoint: `GET /list-cart-items/`

3. **Remove Product from Cart**
   - Endpoint: `POST /remove-from-cart/(?P<product_id>[^/.]+)`

4. **Update Cart Item Quantity**
   - Endpoint: `POST /update-cart-item/(?P<product_id>[^/.]+)`
   - Request Data: `{"quantity": 5}`

5. **Clear Cart**
   - Endpoint: `DELETE /clear-cart/`
