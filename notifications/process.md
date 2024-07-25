Notifications App Process Documentation
Overview
The Notifications app manages notification messages for users. It supports the creation and retrieval of notifications to keep users informed of significant events or updates.

Processes
1. Create a Notification
Description: Generates a notification for a specific user.

Endpoint:

POST /notifications/
Request Body Example:

json
Copy code
{
    "user": 1,
    "message": "Your support message has been received."
}
Process:

A part of the system triggers the creation of a notification (e.g., support app after a support message is created).
The system sends a POST request to the /notifications/ endpoint with the user ID and message.
The server creates a new notification entry in the database and returns the created notification.
2. Retrieve Notifications
Description: Retrieves all notifications for the authenticated user.

Endpoint:

GET /notifications/
Success Response Example:

json
Copy code
[
    {
        "id": 1,
        "message": "Your support message has been received.",
        "created_at": "2024-07-25T12:34:56Z"
    }
]
Process:

The user sends a GET request to the /notifications/ endpoint with appropriate authentication.
The server retrieves and returns a list of notifications associated with the authenticated user.
API Endpoints
POST /notifications/ - Create a new notification.
GET /notifications/ - Retrieve notifications for the authenticated user.