from django.urls import path
from .views import register, login, activate, current_user, resend_verification_email, profile_view, forget_password, reset_password, change_password, logout, CustomTokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('activate/<str:token>/', activate, name='activate_account'),
    path('resend-verification/', resend_verification_email, name='resend_verification'),
    path('current_user/', current_user, name='current_user'),
    path('profile/', profile_view, name='profile'),
    path('forget-password/', forget_password, name='forget_password'),
    path('reset-password/<int:uid>/<str:token>/', reset_password, name='reset_password'),
    path('change-password/', change_password, name='change_password'),
    path('logout/', logout, name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
