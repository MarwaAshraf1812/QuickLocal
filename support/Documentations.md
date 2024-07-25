# Support App Documentation

## Overview

The Support App allows vendors to contact customer support and receive notifications. It provides a system to manage support messages and communicate with the support team effectively.

## Features

- **Contact Support**: Vendors can send support messages.
- **Receive Notifications**: Vendors can receive notifications related to their support messages.

## API Endpoints

### Contact Support

- **Endpoint**: `POST /support/`
- **Description**: Allows vendors to send a support message to the support team.
- **Request Body Example**:
{
    "user": 1,
    "subject": "Issue with Product Return",
    "message": "I need assistance with returning a product I purchased last week. The product is defective."
}
- **Respone Body**:

- Success (201 Created)
 {
    "id": 3,
    "subject": "Issue with Product Return",
    "message": "I need assistance with returning a product I purchased last week. The product is defective.",
    "created_at": "2024-07-25T15:23:10.767788Z",
    "user": 18
}

- Error (400 Bad Request):

{
    "user": ["This field is required."],
    "message": ["This field is required."]
}
