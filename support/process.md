# Support App Process Documentation

## Overview

The Support app allows vendors to contact customer support and receive notifications about their support messages. This document outlines the processes involved in handling support messages, notifications, and related actions.

## Processes

### 1. Contact Support

**Description**: Vendors can contact customer support by submitting a support message.

**Endpoint**:
- **POST** `/support/`

**Request Body Example**:
```json
{
    "message": "I need assistance with my account.",
    "user": 1
}
```

**Success Response (201 Created)**:
```json
{
    "id": 1,
    "message": "I need assistance with my account.",
    "user": 1,
    "created_at": "2024-07-25T12:34:56Z"
}
```

**Failure Response (400 Bad Request)**:
```json
{
    "message": "This field is required."
}
```

**Process**:
1. The vendor submits a support message through the POST request.
2. The support message is saved in the database.
3. A notification is created for the vendor confirming receipt of the message.
4. An email notification is sent to the support team about the new support message.

### 2. Receive Notifications

**Description**: Vendors receive notifications about their support messages.

**Endpoint**:
- **GET** `/notifications/`

**Success Response (200 OK)**:
```json
[
    {
        "id": 1,
        "message": "Your support message has been received.",
        "created_at": "2024-07-25T12:34:56Z"
    }
]
```

**Process**:
1. The vendor retrieves a list of notifications related to their support messages.
2. Notifications include details about the support message status and other relevant information.

### 3. Delete a Support Message

**Description**: Allows deletion of a specific support message.

**Endpoint**:
- **DELETE** `/support/{id}/delete_message/`

**Request Body Example**: Not applicable (no body required for this endpoint).

**Success Response (204 No Content)**:
```json
{
    "message": "Support message deleted successfully"
}
```

**Failure Response (404 Not Found)**:
```json
{
    "error": "Support message not found"
}
```

**Process**:
1. The vendor sends a DELETE request to remove a specific support message by its ID.
2. The support message is deleted from the database.
3. A confirmation message is returned to indicate successful deletion.

### 4. Clear All Support Messages

**Description**: Allows deletion of all support messages for the authenticated vendor.

**Endpoint**:
- **DELETE** `/support/clear_messages/`

**Request Body Example**: Not applicable (no body required for this endpoint).

**Success Response (204 No Content)**:
```json
{
    "message": "X support messages deleted successfully"
}
```

**Process**:
1. The vendor sends a DELETE request to clear all their support messages.
2. All support messages for the authenticated vendor are deleted from the database.
3. A confirmation message is returned with the count of deleted messages.

## API Endpoints

- **POST** `/support/` - Submit a new support message.
- **GET** `/notifications/` - Retrieve notifications for the authenticated vendor.
- **DELETE** `/support/{id}/delete_message/` - Delete a specific support message.
- **DELETE** `/support/clear_messages/` - Delete all support messages for the authenticated vendor.
