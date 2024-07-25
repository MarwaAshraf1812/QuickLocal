from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import SupportMessage
from notifications.models import Notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=SupportMessage)
def notify_support_team(sender, instance, created, **kwargs):
    if created:
        logger.info(f'SupportMessage instance saved: {instance}')

        # Send email to the support team
        send_mail(
            subject=f'New support message from {instance.user.username}',
            message=f'{instance.message}',
            from_email='no-reply@quicklocal.com',
            recipient_list=['applicationdeveloper97@gmail.com'],
        )

        # Send email to the user
        send_mail(
            subject='Your support message has been received',
            message=f'Thank you for reaching out to us, {instance.user.username}. Your message: "{instance.message}" has been received. We will get back to you soon.',
            from_email='no-reply@quicklocal.com',
            recipient_list=[instance.user.email],
        )

        # Create notification for the support team
        Notification.objects.create(
            user=instance.user,
            message=f'New support message from {instance.user.username}'
        )
