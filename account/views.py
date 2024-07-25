from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication #type: ignore
from rest_framework.response import Response #type: ignore
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status #type: ignore
from .models import UserProfile
from .serializers import (
    SignUpSerializer, UserSerializer, UserProfileSerializer,
    ChangePasswordSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny #type: ignore
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken #type: ignore
import logging
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def get_current_host(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{protocol}://{host}/"


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        email = data.get('email')
        username = data.get('username')

        if not User.objects.filter(email=email).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=email,
                username=username,
                password=make_password(data['password']),
                is_active=False
            )

            token = get_random_string(length=32)
            profile = user.userprofile
            profile.activation_token = token
            profile.token_created_at = timezone.now()
            profile.save()

            try:
                host_url = get_current_host(request)
                verification_link = f"{host_url}/activate/{token}/"
                subject = 'Activate Your Account'
                message = f'Hi {user.first_name},\n\nPlease click the link below to activate your account:\n\n{verification_link}'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                print("Email sent")
                return Response(
                    {'details': 'Please check your email to activate your account.'},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                return Response(
                    {'error': f'An error occurred while sending the verification email: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {'error': 'This email already exists!'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def activate(request, token):
    try:
        profile = UserProfile.objects.get(activation_token=token)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)

    if profile.is_token_expired():
        return Response({'error': 'Token has expired!'}, status=status.HTTP_400_BAD_REQUEST)

    user = profile.user
    user.is_active = True
    user.save()
    profile.activation_token = None
    profile.token_created_at = None
    profile.save()

    return Response({'details': 'Your account has been activated successfully!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Both email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_active:
        return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate new tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    response = Response({
        'refresh': str(refresh),
        'access': access_token,
        'redirect': '/profile/'
    }, status=status.HTTP_200_OK)
    
    # Set new tokens in cookies
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAMESITE,
        max_age=300,  # 1 hour
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAMESITE,
        max_age=3600 * 24 * 10,  # 10 days
    )

    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if user.is_active:
        return Response({'details': 'This email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a new verification token
    token = get_random_string(length=32)
    profile = user.userprofile
    profile.activation_token = token
    profile.token_created_at = datetime.now()
    profile.save()

    # Send verification email
    host_url = get_current_host(request)
    verification_link = f"{host_url}/activate/{token}/"
    subject = 'Activate Your Account'
    message = f'Hi {user.first_name},\n\nPlease click the link below to activate your account:\n\n{verification_link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

    return Response({'details': 'A new verification email has been sent.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Retrieve the current authenticated user's details.
    Returns:
        Response: Serialized user data.
    """
    try:
        user = UserSerializer(request.user, many=False)
        return Response(user.data)
    except Exception as e:
        logger.error(f"Error retrieving current user: {e}")
        return Response({'error': 'An error occurred while retrieving user details.'}, status=500)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your profile has been updated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def forget_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    token = default_token_generator.make_token(user)
    reset_link = f"{get_current_host(request)}reset-password/{user.pk}/{token}/"

    subject = 'Password Reset Requested'
    message = f'Hi {user.first_name},\n\nPlease click the link below to reset your password:\n\n{reset_link}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

    return Response({'details': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({
            'error': 'Invalid token or user ID. Please try the forgot password process again.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({
            'error': 'Invalid token. Please try the forgot password process again.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Assuming the request contains the new password
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if new_password and confirm_password:
        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'details': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'New password and confirmation are required.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Password has been changed successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def logout(request):
    # Retrieve the refresh token from cookies
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create RefreshToken instance and blacklist it
        token = RefreshToken(refresh_token)
        token.blacklist()  # Ensure blacklisting is supported in your configuration

        # Clear tokens from cookies
        response = Response({'success': 'User logged out successfully'}, status=status.HTTP_200_OK)

        # Delete cookies by setting expired values
        response.set_cookie(
            key='access_token',
            value='',
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
        )
        response.set_cookie(
            key='refresh_token',
            value='',
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
        )

        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token not found in cookies."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'refresh': refresh_token}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            return self._check_token(serializer)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def _check_token(self, serializer):
        try:
            validated_data = serializer.validated_data
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response(validated_data, status=status.HTTP_200_OK)
        
        # Delete old cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        # Set new tokens in cookies
        response.set_cookie(
            key='access_token',
            value=validated_data['access'],
            httponly=True,
            secure=False,   # Update to True in production
            samesite='Lax',
            path='/',
            max_age=3600    # Set cookie expiration as needed
        )
        response.set_cookie(
            key='refresh_token',
            value=validated_data['refresh'],
            httponly=True,
            secure=False,   # Update to True in production
            samesite='Lax',
            path='/',
            max_age=3600 * 24 * 10  # Set cookie expiration as needed
        )
        return response
