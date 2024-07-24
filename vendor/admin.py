from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'contact_email', 'address', 'phone', 'created_at', 'updated_at')
    search_fields = ('name', 'contact_email', 'phone')
    list_filter = ('created_at', 'updated_at')
    ordering = ('created_at',)