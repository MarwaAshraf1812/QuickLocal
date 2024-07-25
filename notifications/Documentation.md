Notifications App Documentation
Overview
The Notifications app handles the creation and retrieval of notifications for users within the system. It is designed to keep users informed about relevant events, such as receiving support messages.

Models
Notification
id: Integer, Auto-generated ID
user: ForeignKey, Reference to the User model
message: Text, Notification content
created_at: DateTime, Timestamp of when the notification was created
API Endpoints
1. Retrieve Notifications
Endpoint: GET /notifications/

Description: Retrieves a list of notifications for the authenticated user.

Request Headers:

Authorization: Bearer <token>
Success Response (200 OK):

json
Copy code
[
    {
        "id": 1,
        "message": "Your support message has been received.",
        "created_at": "2024-07-25T12:34:56Z"
    }
]
Failure Response (401 Unauthorized):

json
Copy code
{
    "detail": "Authentication credentials were not provided."
}
Process:

The user sends a GET request to retrieve their notifications.
The server returns a list of notifications related to the user.
2. Create Notification
Endpoint: POST /notifications/

Description: Creates a new notification for a user.

Request Body Example:

json
Copy code
{
    "user": 1,
    "message": "Your support message has been received."
}
Success Response (201 Created):

json
Copy code
{
    "id": 1,
    "user": 1,
    "message": "Your support message has been received.",
    "created_at": "2024-07-25T12:34:56Z"
}
Failure Response (400 Bad Request):

json
Copy code
{
    "message": "This field is required."
}
Process:

The system creates a new notification entry in the database for the specified user.
The server returns the newly created notification.
Usage
Sending Notifications
Notifications are created by various parts of the system, such as the support app, when certain events occur (e.g., a new support message).

Managing Notifications
Users can retrieve their notifications through the GET endpoint to view messages and stay updated on relevant activities.