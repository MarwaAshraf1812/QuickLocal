from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=64, null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_created_at = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone Number"))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("State"))
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("ZIP Code"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name=_("Profile Picture"))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Gender"))
    preferred_language = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Preferred Language"))
    currency = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Currency"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Joined"))
    last_login = models.DateTimeField(auto_now=True, verbose_name=_("Last Login"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))
    order_history = models.TextField(blank=True, null=True, verbose_name=_("Order History"))

    def is_token_expired(self):
        if self.token_created_at:
            expiration_time = self.token_created_at + timedelta(hours=2)  # Token valid for 48 hours
            return timezone.now() > expiration_time
        return True  # Treat as expired if token_created_at is not set or invalid
    
    def is_reset_token_expired(self):
        if self.reset_token_created_at:
            expiration_time = self.reset_token_created_at + timedelta(hours=1)  # Token valid for 1 hour
            return timezone.now() > expiration_time
        return True  # Treat as expired if reset_token_created_at is not set or invalid

    def __str__(self):
        return self.user.username
