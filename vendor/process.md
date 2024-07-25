Process Description

1. Vendor Registration and Onboarding

    Sign Up:

        Vendor signs up via a registration form.
        Data: Name, contact email, phone number, address.
        Verification:

        Vendor verifies email.
        System may require admin approval.
    Account Setup:

        Vendor logs in and completes profile setup.

    API Endpoints:

        POST /register/
        POST /verify-email/
        POST /login/
        PUT /vendor/profile/

2. Product Management

    Add New Products:

        Vendor adds new products.
        Data: Product name, description, price, images, stock quantity.

    Edit Products:
        Vendor edits existing products.

    Delete Products:
        Vendor deletes products.

    Manage Product Categories:
        Vendor categorizes products.

    API Endpoints:

        POST /products/
        PUT /products/{id}/
        DELETE /products/{id}/
        GET /products/categories/

3. Order Management

    View Orders:
        Vendor views orders.

    Update Order Status:
        Vendor updates order status.

    Handle Returns and Refunds:
        Vendor processes returns and refunds.

    API Endpoints:

        GET /orders/
        PUT /orders/{id}/status/
        POST /orders/{id}/refund/

4. Financial Management
    View Sales Reports:
        Vendor views sales performance reports.

    Manage Payments:
        Vendor checks payment status.

    API Endpoints:
        GET /sales/reports/
        GET /payments/

5. Communication and Support
    Contact Support:
        Vendor contacts customer support.
        Receive Notifications:
        Vendor receives notifications.

    API Endpoints:
        POST /support/
        GET /notifications/

6. Account Management
    Update Profile Information:
        Vendor updates profile details.

    Change Password:
        Vendor changes account password.
        Review Account Activity:
        Vendor reviews account activity.

    API Endpoints:

        PUT /vendor/profile/
        POST /change-password/
        GET /account/activity/
