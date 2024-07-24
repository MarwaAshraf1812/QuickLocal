from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Signal to create or update UserProfile when User is created or updated


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        profile.date_joined = instance.date_joined
        profile.last_login = instance.last_login
        profile.is_verified = instance.is_active
        profile.save()
