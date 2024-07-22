### Orders App Documentation

#### Process for Creating an Order

1. **Receive Cart Data**: Extract cart data and stripe token from the request body.
2. **Validate Data**: Validate the data using `CreateOrderSerializer`.
3. **Create Order**: Instantiate and save a new `Order` object with user and order details.
4. **Create Order Items**: For each item in the cart, create and save an `OrderItem` linked to the newly created `Order`.
5. **Calculate Totals**: Calculate the total amount and total items for the order.
6. **Save Order**: Save the total amount in the `Order` object.
7. **Clear Cart**: Optionally, clear the user's cart after the order is created.
8. **Create Stripe PaymentIntent**: Create a Stripe PaymentIntent for the order.
9. **Return Response**: Return a response with the order details, total amount, total items, and Stripe client secret.

#### Process for Retrieving User Orders

1. **Check Authentication**: Ensure the user is authenticated.
2. **Fetch Orders**: Retrieve all orders associated with the authenticated user.
3. **Serialize Orders**: Serialize the orders data.
4. **Return Response**: Return the serialized orders in the response.

#### Process for Retrieving Order Details

1. **Receive Order ID**: Extract the order ID from the URL.
2. **Fetch Order**: Retrieve the order object using the order ID.
3. **Serialize Order**: Serialize the order data.
4. **Return Response**: Return the serialized order in the response.

#### Process for Listing All Orders (Admin Only)

1. **Fetch All Orders**: Retrieve all orders from the database.
2. **Serialize Orders**: Serialize the orders data.
3. **Return Response**: Return the serialized orders in the response.

#### Process for Updating an Order

1. **Receive Order ID**: Extract the order ID from the URL.
2. **Fetch Order**: Retrieve the order object using the order ID.
3. **Validate Data**: Validate the data using `UpdateOrderSerializer`.
4. **Update Order**: Update the order with the new data.
5. **Serialize Order**: Serialize the updated order data.
6. **Return Response**: Return the serialized order in the response.

#### Process for Deleting an Order

1. **Receive Order ID**: Extract the order ID from the URL.
2. **Fetch Order**: Retrieve the order object using the order ID.
3. **Delete Order**: Delete the order from the database.
4. **Return Response**: Return a success message in the response.
