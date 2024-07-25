from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vendor.models import Vendor

class Command(BaseCommand):
    help = 'Create a vendor for a staff user using user ID'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID of the staff member')
        parser.add_argument('name', type=str, help='Name of the vendor')
        parser.add_argument('contact_email', type=str, help='Contact email of the vendor')

    def handle(self, *args, **options):
        user_id = options['user_id']
        name = options['name']
        contact_email = options['contact_email']

        try:
            user = User.objects.get(id=user_id)
            if not user.is_staff:
                self.stdout.write(self.style.ERROR(f"User with ID '{user_id}' is not a staff member. Cannot create vendor."))
                return

            # Ensure the field names match the Vendor model
            vendor, created = Vendor.objects.get_or_create(
                user=user,
                defaults={'name': name, 'contact_email': contact_email}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Vendor '{name}' created successfully."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Vendor '{name}' already exists."))

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID '{user_id}' does not exist."))