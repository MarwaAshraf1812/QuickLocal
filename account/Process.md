# **Account App Process Documentation**

## **User Experience Overview**

The Account App provides user account management functionalities including registration, activation, login, profile management, password recovery, and logout. Below is a detailed user story flow for each process, incorporating the endpoints and interactions with various components like cookies, custom authentication backends, signals, and middleware.

## User Story and Process Flow ##

## 1. User Registration ##

`Endpoint:` POST /register/

`User Story:`
- A new user signs up by providing their first name, last name, email, username, and password.
- Upon successful registration, an email verification link is sent to the provided email address.
- The user needs to activate their account via the link to complete registration.

`Process:`
1. **Request Handling:**
   - User submits registration details to the /register/ endpoint.
   - **View:** register(request) in views.py.
   - **Serializer:** SignUpSerializer validates and processes the data.

2. **Profile Creation:**
   - A UserProfile is created or updated with an activation token.
   - **Signal:** create_or_update_user_prof
   ile(sender, instance, created, ****kwargs) in signals.py.

3. **Email Verification:**
   - An activation email with a link containing the activation token is sent to the user.
   - **Utility Function:** get_current_host(request) generates the host URL for the activation link.
   - **Email Sending:** send_mail sends the verification email.

**Cookies:**
- No cookies are used during registration.

## 2. Account Activation ##

`Endpoint:` POST /activate/<str:token>/

`User Story:`
- The user clicks the activation link received in the email.
- The system validates the activation token and activates the user's account.

`Process:`
1. **Request Handling:**
   - User accesses the activation link which triggers a POST request to /activate/<token>/.
   - **View:** activate(request, token) in views.py.

2. **Token Validation:**
   - The activation token is validated and the user’s account is activated.

**Cookies:**
- No cookies are used during activation.

## 3. User Login ##

`Endpoint:` POST /login/

`User Story:`
- The user logs in using their email and password.
- On successful login, an access token and a refresh token are issued and stored in cookies.
- The user is redirected to their profile.

`Process:`
1. **Request Handling:**
   - User submits login credentials to /login/.
   - **View:** login(request) in views.py.
   - **Authentication:** EmailBackend in backends.py is used to authenticate the user.

2. **Token Generation:**
   - Refresh and access tokens are generated using RefreshToken.for_user(user).

3. **Token Storage:**
   - Tokens are stored in cookies for subsequent requests.
   - **Cookies:** access_token and refresh_token are set in the response using response.set_cookie.

**Cookies:**
- access_token and refresh_token are set as cookies with attributes httponly, secure, and samesite.

## 4. User Profile Management ##

`Endpoint:` GET /profile/ and POST /profile/

`User Story:`
- Authenticated users can view and update their profile information.
- Profile updates are saved to the UserProfile model.

`Process:`
1. **Request Handling:**
   - **GET Request:** Retrieves the user profile.
     - **View:** profile_view(request) in views.py.
   - **POST Request:** Updates user profile information.
     - **View:** profile_view(request) in views.py.
     - **Serializer:** UserProfileSerializer processes the data.

2. **Profile Retrieval/Update:**
   - **Signal:** create_or_update_user_profile(sender, instance, created, ****kwargs) ensures the UserProfile is up-to-date.

**Cookies:**
- No cookies are used directly for profile management.

## 5. Password Recovery ##

`Endpoint:` POST /forget-password/

`User Story:`
- The user requests a password reset link.
- An email with a reset link is sent to the user's email address.

`Process:`
1. **Request Handling:**
   - User submits their email to /forget-password/.
   - **View:** forget_password(request) in views.py.
   - **Email Sending:** A password reset email is sent with a link containing a token.

2. **Token Handling:**
   - The link includes a token used to verify the password reset request.

**Cookies:**
- No cookies are used during password recovery.

## 6. Password Reset ##

`Endpoint:` POST /reset-password/<int:uid>/<str:token>/

`User Story:`
- The user clicks on the password reset link received via email.
- They provide a new password, which is validated and updated.

`Process:`
1. **Request Handling:**
   - User submits the new password to /reset-password/<uid>/<token>/.
   - **View:** reset_password(request, uid, token) in views.py.
   - **Token Validation:** The token is validated, and the password is updated if the token is valid.

**Cookies:**
- No cookies are used during password reset.

## 7. Change Password ##

`Endpoint:` POST /change-password/

`User Story:`
- Authenticated users can change their current password.

`Process:`
1. **Request Handling:**
   - User submits current and new passwords to /change-password/.
   - **View:** change_password(request) in views.py.
   - **Serializer:** ChangePasswordSerializer validates and updates the password.

**Cookies:**
- No cookies are used during password change.

## 8. User Logout ##

`Endpoint:` POST /logout/

`User Story:`
- The user logs out, which involves invalidating the refresh token and clearing cookies.

`Process:`
1. **Request Handling:**
   - User sends a request to /logout/.
   - **View:** logout(request) in views.py.
   - **Token Blacklisting:** The refresh token is blacklisted using RefreshToken(refresh_token).blacklist().

2. **Cookie Clearing:**
   - Cookies (access_token and refresh_token) are cleared by setting expired values.
   - **Cookies:** Deleted using response.set_cookie with expired values.

### **Custom Authentication and Middleware**

**1. Authentication Backend**

**File:** backends.py

- **Class:** EmailBackend handles authentication using email instead of username.

**2. Middleware**

**File:** auth.py

- **Class:** TokenRefreshMiddleware checks if an access token is missing and attempts to refresh it using the refresh token from cookies.

**3. Signals**

**File:** signals.py

- **Signal:** create_or_update_user_profile creates or updates the UserProfile when the User model is saved.

**4. Custom JWT Authentication**

**File:** backends.py

- **Class:** CookieJWTAuthentication manages JWT authentication using tokens from cookies.

**5. Custom Token Refresh View**

**File:** views.py

- **Class:** CookieTokenRefreshView handles refreshing tokens and updating cookies with new tokens.

---
