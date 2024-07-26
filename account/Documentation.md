### Account Management System Documentation ###

**Overview**

This system handles user account operations, including registration, authentication, and profile management using Django and Django REST Framework.

## Models.py ##
================
### UserProfile Model Documentation

#### Overview
The UserProfile model extends the default Django User model to include additional user-specific information and functionalities, such as account verification tokens, personal details, and preferences.

#### Fields

1. **user**
   - **Type**: OneToOneField(User, on_delete=models.CASCADE)
   - **Description**: A one-to-one relationship with Django's built-in User model. Ensures that each UserProfile is linked to exactly one User.
   - **Validation**: No additional validation. Required to maintain consistency with the User model.

2. **activation_token**
   - **Type**: CharField(max_length=64, null=True, blank=True)
   - **Description**: Stores the activation token used for account verification.
   - **Validation**: Must be a string with a maximum length of 64 characters.

3. **token_created_at**
   - **Type**: DateTimeField(null=True, blank=True)
   - **Description**: Timestamp of when the activation token was created.
   - **Validation**: No additional validation. Can be null or blank.

4. **reset_password_token**
   - **Type**: CharField(max_length=64, null=True, blank=True)
   - **Description**: Stores the token used for password reset requests.
   - **Validation**: Must be a string with a maximum length of 64 characters.

5. **reset_token_created_at**
   - **Type**: DateTimeField(null=True, blank=True)
   - **Description**: Timestamp of when the reset password token was created.
   - **Validation**: No additional validation. Can be null or blank.

6. **phone_number**
   - **Type**: CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone Number"))
   - **Description**: User's phone number.
   - **Validation**: Must be a string with a maximum length of 15 characters.

7. **address**
   - **Type**: CharField(max_length=255, blank=True, null=True, verbose_name=_("Address"))
   - **Description**: User's address.
   - **Validation**: Must be a string with a maximum length of 255 characters.

8. **city**
   - **Type**: CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))
   - **Description**: User's city of residence.
   - **Validation**: Must be a string with a maximum length of 100 characters.

9. **state**
   - **Type**: CharField(max_length=100, blank=True, null=True, verbose_name=_("State"))
   - **Description**: User's state or province.
   - **Validation**: Must be a string with a maximum length of 100 characters.

10. **zip_code**
    - **Type**: CharField(max_length=20, blank=True, null=True, verbose_name=_("ZIP Code"))
    - **Description**: User's postal or ZIP code.
    - **Validation**: Must be a string with a maximum length of 20 characters.

11. **country**
    - **Type**: CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))
    - **Description**: User's country of residence.
    - **Validation**: Must be a string with a maximum length of 100 characters.

12. **profile_picture**
    - **Type**: ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name=_("Profile Picture"))
    - **Description**: User's profile picture.
    - **Validation**: Allows file uploads. Can be blank or null.

13. **date_of_birth**
    - **Type**: DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    - **Description**: User's date of birth.
    - **Validation**: Can be blank or null.

14. **gender**
    - **Type**: CharField(max_length=10, blank=True, null=True, verbose_name=_("Gender"))
    - **Description**: User's gender.
    - **Validation**: Must be a string with a maximum length of 10 characters.

15. **preferred_language**
    - **Type**: CharField(max_length=50, blank=True, null=True, verbose_name=_("Preferred Language"))
    - **Description**: User's preferred language for communication.
    - **Validation**: Must be a string with a maximum length of 50 characters.

16. **currency**
    - **Type**: CharField(max_length=10, blank=True, null=True, verbose_name=_("Currency"))
    - **Description**: User's preferred currency.
    - **Validation**: Must be a string with a maximum length of 10 characters.

17. **date_joined**
    - **Type**: DateTimeField(auto_now_add=True, verbose_name=_("Date Joined"))
    - **Description**: Timestamp of when the user joined.
    - **Validation**: Automatically set to the current date and time when the profile is created.

18. **last_login**
    - **Type**: DateTimeField(auto_now=True, verbose_name=_("Last Login"))
    - **Description**: Timestamp of the last login.
    - **Validation**: Automatically updated to the current date and time on each login.

19. **is_verified**
    - **Type**: BooleanField(default=False, verbose_name=_("Is Verified"))
    - **Description**: Indicates whether the user's account is verified.
    - **Validation**: Defaults to False.

20. **order_history**
    - **Type**: TextField(blank=True, null=True, verbose_name=_("Order History"))
    - **Description**: Stores a textual representation of the user's order history.
    - **Validation**: Can be blank or null.

#### Methods

1. **is_token_expired()**
   - **Description**: Checks if the activation token has expired.
   - **Implementation**: Compares the current time with the token creation time plus a validity period (2 hours).
   - **Returns**: True if the token is expired or if token_created_at is not set; otherwise, False.

2. **is_reset_token_expired()**
   - **Description**: Checks if the password reset token has expired.
   - **Implementation**: Compares the current time with the reset token creation time plus a validity period (1 hour).
   - **Returns**: True if the token is expired or if reset_token_created_at is not set; otherwise, False.

3. **_str_()**
   - **Description**: Returns a string representation of the UserProfile.
   - **Implementation**: Uses the associated User's username.
   - **Returns**: The username of the user associated with the profile.

## Serializers.py ##
====================

#### SignUpSerializer
The SignUpSerializer handles user registration by validating and creating new user accounts.

##### Fields
- **first_name**: Required. The first name of the user.
- **last_name**: Required. The last name of the user.
- **username**: Required. The username for the user account.
- **email**: Required. The email address of the user.
- **password**: Required. The password for the user account. Must be at least 8 characters long.
- **confirm_password**: Write-only field. Used to confirm the password. Must match the password field.

##### Validations
- **Password Matching**: Ensures that password and confirm_password fields match. Raises a validation error if they do not.
- **Password Complexity**: Uses Django's validate_password to enforce password complexity requirements.

##### Methods
- **validate(attrs)**: Custom validation method that checks if password matches confirm_password and validates the password complexity.
- **create(validated_data)**: Creates a new User instance using User.objects.create_user after removing the confirm_password field from validated_data.

---

#### UserSerializer
The UserSerializer is used for serializing user data for API responses, including computed fields for improved data representation.

##### Fields
- **id**: The unique identifier for the user.
- **first_name**: The first name of the user.
- **last_name**: The last name of the user.
- **email**: The email address of the user.
- **username**: The username of the user.
- **full_name**: A computed field that concatenates first_name and last_name, or defaults to username.

##### Methods
- **get_full_name(obj)**: Computes the full name of the user. Returns the concatenation of first_name and last_name, or defaults to username if the name fields are empty.
- **to_representation(instance)**: Overrides the default serialization to ensure email and username are represented in lowercase for consistency.

---

#### UserProfileSerializer
The UserProfileSerializer handles the serialization of UserProfile model instances.

##### Fields
- **phone_number**: The phone number of the user.
- **address**: The address of the user.
- **city**: The city of the user's residence.
- **state**: The state or province of the user's residence.
- **zip_code**: The postal or ZIP code of the user's address.
- **country**: The country of the user's residence.
- **profile_picture**: The profile picture of the user.
- **date_of_birth**: The user's date of birth.
- **gender**: The gender of the user.
- **preferred_language**: The user's preferred language for communication.
- **currency**: The user's preferred currency.

---

#### ChangePasswordSerializer
The ChangePasswordSerializer handles password change requests.

##### Fields
- **old_password**: Required. The current password of the user.
- **new_password**: Required. The new password for the user account.
- **confirm_password**: Required. Confirmation of the new password. Must match the new_password field.

##### Validations
- **Old Password Check**: Verifies that the provided old_password matches the current password of the user.
- **New Password Matching**: Ensures that new_password and confirm_password match. Raises a validation error if they do not.
- **New Password Complexity**: Validates that the new_password meets complexity requirements using Django's validate_password.

##### Methods
- **validate(attrs)**: Custom validation method that checks old password validity, ensures new password and confirmation match, and validates new password complexity.
- **save()**: Updates the user’s password with the new password and saves the user instance.

### Authentication and Middleware Documentation

## Backends.py ##
====================

**EmailBackend**
The EmailBackend class extends ModelBackend to authenticate users using their email address instead of their username.

##### Methods

- **authenticate(self, request, username=None, password=None, **kwargs)**
  - ``Purpose``: Authenticates a user based on their email address.
  - **Parameters**:
    - request: The HTTP request object.
    - username: The email address used for authentication. If None, it retrieves from kwargs.
    - password: The password provided for authentication.
    - **kwargs: Additional keyword arguments.
  - **Returns**: A User object if authentication is successful; otherwise, None.

- **get_user(self, user_id)**
  - ``Purpose``: Retrieves a User instance by its primary key.
  - **Parameters**:
    - user_id: The primary key of the user.
  - **Returns**: A User object if found; otherwise, None.

---

## Auth.py ##
====================

**CookieJWTAuthentication**
The CookieJWTAuthentication class extends JWTAuthentication to handle JWT authentication from cookies and headers.

##### Methods

- **authenticate(self, request)**
  - ``Purpose``: Authenticates a user based on the JWT provided in cookies or Authorization header.
  - **Parameters**:
    - request: The HTTP request object.
  - **Returns**: A tuple (user, validated_token) if authentication is successful; otherwise, None.
  - **Logging**:
    - Logs the presence of access tokens in cookies or headers.
    - Logs success or failure of token validation.

---

## Middleware.py ##
====================

**TokenRefreshMiddleware**
The TokenRefreshMiddleware class handles token refreshing by intercepting requests and attempting to refresh expired access tokens using a refresh token.

##### Methods

- **process_request(self, request)**
  - ``Purpose``: Checks for an expired access token and attempts to refresh it using the refresh token.
  - **Parameters**:
    - request: The HTTP request object.
  - **Returns**: None.
  - **Logging**:
    - Logs attempts to refresh tokens and their success or failure.

- **process_response(self, request, response)**
  - ``Purpose``: Adds or updates the access token in the response cookies.
  - **Parameters**:
    - request: The HTTP request object.
    - response: The HTTP response object.
  - **Returns**: The updated response object.
  - **Cookie Attributes**:
    - Sets the access_token cookie with httponly, secure, samesite='Lax', and max_age=300 attributes.


## Signals.py ##
====================

``Purpose``
The signals.py file contains Django signals that manage the creation and updating of UserProfile instances in relation to User model events.

---

**Signal Handlers**

- **create_or_update_user_profile**
  - **Signal**: post_save
  - **Sender**: User
  - ``Purpose``: Ensures a UserProfile is created or updated when a User instance is created or updated.
  - **Parameters**:
    - sender: The model class that sent the signal (User in this case).
    - instance: The actual instance of the model being saved (User instance).
    - created: Boolean indicating whether the instance is being created (True) or updated (False).
    - **kwargs: Additional keyword arguments provided by the signal.
  - **Behavior**:
    - **On Creation**: Creates a new UserProfile instance linked to the newly created User.
    - **On Update**: Retrieves or creates a UserProfile instance linked to the updated User, updates profile fields (date_joined, last_login, is_verified), and saves the profile.

---

**Details**

- **Signal**: The post_save signal is dispatched after a model’s save() method is called, either for creation or update.
- **Usage**: This signal ensures that every User has an associated UserProfile, and that the UserProfile is kept up-to-date with relevant fields from the User model.

---

## Views.py ##
===============

``Purpose``
The views.py file contains view functions and class-based views for user authentication, registration, and profile management.

---

**Views**

1. **register**
   - ``Endpoint``: /register/
   - ``Method``: POST
   - ``Purpose``: Registers a new user and sends an activation email.
   - ``Request Data``:
     - first_name: User's first name.
     - last_name: User's last name.
     - email: User's email address.
     - username: User's username.
     - password: User's password.
   - ``Response``:
     - **Success**: { 'details': 'Please check your email to activate your account.' } (HTTP 201 Created)
     - **Error**: { 'error': 'This email already exists!' } (HTTP 400 Bad Request)
     - **Error**: { 'error': 'An error occurred while sending the verification email: {error}' } (HTTP 500 Internal Server Error)
   - ``Validations``:
     - Checks if the email already exists.
     - Ensures email is unique before creating a user.
   - ``Error Messages``:
     - If email exists: 'This email already exists!'
     - If email sending fails: Detailed error message

2. **activate**
   - ``Endpoint``: /activate/<str:token>/
   - ``Method``: POST
   - ``Purpose``: Activates a user's account using an activation token.
   - ``Request Data``:
     - token: Activation token sent to the user's email.
   - ``Response``:
     - **Success**: { 'details': 'Your account has been activated successfully!' } (HTTP 200 OK)
     - **Error**: { 'error': 'Invalid token!' } (HTTP 400 Bad Request)
     - **Error**: { 'error': 'Token has expired!' } (HTTP 400 Bad Request)
   - ``Validations``:
     - Checks if the token is valid and not expired.
   - ``Error Messages``:
     - If token is invalid or expired: Appropriate error message

3. **login**
   - ``Endpoint``: /login/
   - ``Method``: POST
   - ``Purpose``: Authenticates a user and provides JWT tokens.
   - ``Request Data``:
     - email: User's email address.
     - password: User's password.
   - ``Response``:
     - **Success**: { 'refresh': 'refresh_token', 'access': 'access_token', 'redirect': '/profile/' } (HTTP 200 OK)
     - **Error**: { 'error': 'Both email and password are required.' } (HTTP 400 Bad Request)
     - **Error**: { 'error': 'User with this email does not exist.' } (HTTP 404 Not Found)
     - **Error**: { 'error': 'Please verify your email before logging in.' } (HTTP 401 Unauthorized)
     - **Error**: { 'error': 'Invalid email or password' } (HTTP 401 Unauthorized)
   - ``Validations``:
     - Checks if both email and password are provided.
     - Validates email and password.
   - ``Error Messages``:
     - If credentials are incorrect or user is inactive: Appropriate error message

4. **resend_verification_email**
   - ``Endpoint``: /resend-verification/
   - ``Method``: POST
   - ``Purpose``: Resends the activation email for verification.
   - ``Request Data``:
     - email: User's email address.
   - ``Response``:
     - **Success**: { 'details': 'A new verification email has been sent.' } (HTTP 200 OK)
     - **Error**: { 'error': 'User with this email does not exist.' } (HTTP 404 Not Found)
     - **Error**: { 'details': 'This email is already verified.' } (HTTP 400 Bad Request)
   - ``Validations``:
     - Ensures that an email is associated with an inactive user.
   - ``Error Messages``:
     - If email does not exist or is already verified: Appropriate error message

5. **current_user**
   - ``Endpoint``: /current_user/
   - ``Method``: GET
   - ``Purpose``: Retrieves details of the currently authenticated user.
   - ``Response``:
     - **Success**: Serialized user data (HTTP 200 OK)
     - **Error**: { 'error': 'An error occurred while retrieving user details.' } (HTTP 500 Internal Server Error)
   - ``Validations``:
     - Ensures the user is authenticated.
   - ``Error Messages``:
     - If there's an issue retrieving user details: Detailed error message

6. **profile_view**
   - ``Endpoint``: /profile/
   - ``Method``: GET, POST
   - ``Purpose``: Retrieves or updates the user's profile.
   - ``Request Data`` (for POST):
     - Data fields to update in UserProfile.
   - ``Response``:
     - **GET Success**: Serialized user profile data (HTTP 200 OK)
     - **POST Success**: { 'message': 'Your profile has been updated successfully!' } (HTTP 200 OK)
     - **Error**: { 'error': 'An error occurred while retrieving profile details.' } (HTTP 500 Internal Server Error)
     - **Error**: { 'error': 'Profile update failed due to invalid data.' } (HTTP 400 Bad Request)
   - ``Validations``:
     - Ensures the profile data is valid for updates.
   - ``Error Messages``:
     - If profile update fails: Detailed error message

7. **forget_password**
   - ``Endpoint``: /forget-password/
   - ``Method``: POST
   - ``Purpose``: Sends a password reset link to the user's email.
   - ``Request Data``:
     - email: User's email address.
   - ``Response``:
     - **Success**: { 'details': 'Password reset link has been sent to your email.' } (HTTP 200 OK)
     - **Error**: { 'error': 'User with this email does not exist.' } (HTTP 404 Not Found)
   - ``Validations``:
     - Checks if the email is associated with an existing user.
   - ``Error Messages``:
     - If email does not exist: Appropriate error message

8. **reset_password**
   - ``Endpoint``: /reset-password/<int:uid>/<str:token>/
   - ``Method``: POST
   - ``Purpose``: Resets the user's password using a reset token.
   - ``Request Data``:
     - new_password: New password.
     - confirm_password: Confirm new password.
   - ``Response``:
     - **Success**: { 'details': 'Password has been reset successfully.' } (HTTP 200 OK)
     - **Error**: { 'error': 'Invalid token or user ID. Please try the forgot password process again.' } (HTTP 400 Bad Request)
     - **Error**: { 'error': 'Invalid token. Please try the forgot password process again.' } (HTTP 400 Bad Request)
     - **Error**: { 'error': 'Passwords do not match.' } (HTTP 400 Bad Request)
   - ``Validations``:
     - Checks if the reset token is valid.
     - Ensures new passwords match.
   - ``Error Messages``:
     - If token or user ID is invalid or passwords do not match: Appropriate error message

9. **change_password**
   - ``Endpoint``: /change-password/
   - ``Method``: POST
   - ``Purpose``: Changes the password for the currently authenticated user.
   - ``Request Data``:
     - old_password: Current password.
     - new_password: New password.
     - confirm_password: Confirm new password.
   - ``Response``:
     - **Success**: { 'detail': 'Password has been changed successfully.' } (HTTP 200 OK)
     - **Error**: { 'error': 'Invalid old password or new passwords do not match.' } (HTTP 400 Bad Request)
   - ``Validations``:
     - Ensures the old password is correct.
     - Checks if new passwords match.
   - ``Error Messages``:
     - If old password is incorrect or new passwords do not match: Appropriate error message

10. **logout**
    - ``Endpoint``: /logout/
    - ``Method``: POST
    - ``Purpose``: Logs out the user by blacklisting the refresh token and clearing cookies.
    - ``Response``:
      - **Success**: { 'success': 'User logged out successfully' } (HTTP 200 OK)
      - **Error**: { 'error': 'Refresh token is required' } (HTTP 400 Bad Request)
      - **Error**: { 'error': '{error}' } (HTTP 500 Internal Server Error)
    - ``Validations``:
      - Ensures a refresh token is present.
    - ``Error Messages``:
      - If refresh token is missing or logout fails: Appropriate error message


11. **CookieTokenRefreshView**
    - ``Endpoint``: /token/refresh/
    - ``Method``: POST
    - ``Purpose``: Refreshes the JWT access token and sets it as a cookie.
    - ``Request Data``:
      - refresh: Refresh token.
    - ``Response``:
      - **Success**: { 'access': 'new_access_token' } (HTTP 200 OK)
      - **Error**: { 'error': 'Invalid refresh token.' } (HTTP 400 Bad Request)
      - **Error**: { 'error': 'Token has expired.' } (HTTP 400 Bad Request)
    - ``Validations``:
      - Checks if the refresh token is valid.
    - ``Error Messages``:
      - If refresh token is invalid or expired: Appropriate error message

---

## Urls.py ##
===============

**Purpose**
The urls.py file maps URLs to the corresponding view functions or class-based views.

---

**URL Patterns**

1. **register**
   - **URL**: /register/
   - **View**: register
   - **Method**: POST
   - **Purpose**: Handles user registration.

2. **activate**
   - **URL**: /activate/<str:token>/
   - **View**: activate
   - **Method**: POST
   - **Purpose**: Activates user account with the provided token.

3. **login**
   - **URL**: /login/
   - **View**: login
   - **Method**: POST
   - **Purpose**: Authenticates a user and returns JWT tokens.

4. **resend_verification_email**
   - **URL**: /resend-verification/
   - **View**: resend_verification_email
   - **Method**: POST
   - **Purpose**: Resends the activation email.

5. **current_user**
   - **URL**: /current_user/
   - **View**: current_user
   - **Method**: GET
   - **Purpose**: Retrieves details of the current authenticated user.

6. **profile_view**
   - **URL**: /profile/
   - **View**: profile_view
   - **Method**: GET, POST
   - **Purpose**: Retrieves or updates the user's profile.

7. **forget_password**
   - **URL**: /forget-password/
   - **View**: forget_password
   - **Method**: POST
   - **Purpose**: Sends a password reset link to the user's email.

8. **reset_password**
   - **URL**: /reset-password/<int:uid>/<str:token>/
   - **View**: reset_password
   - **Method**: POST
   - **Purpose**: Resets the user's password using a reset token.

9. **change_password**
   - **URL**: /change-password/
   - **View**: change_password
   - **Method**: POST
   - **Purpose**: Changes the password for the currently authenticated user.

10. **logout**
    - **URL**: /logout/
    - **View**: logout
    - **Method**: POST
    - **Purpose**: Logs out the user by invalidating the refresh token.

11. **CookieTokenRefreshView**
    - **URL**: /token/refresh/
    - **View**: CookieTokenRefreshView
    - **Method**: POST
    - **Purpose**: Refreshes the JWT access token and sets it as a cookie.

---
