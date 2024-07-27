from django.contrib import admin
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    fields = ['product', 'price', 'quantity']
    extra = 1 # Number of empty forms to display initially


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'order_status',
                    'created', 'updated']
    list_filter = ['order_status', 'created', 'updated']
    inlines = [OrderItemInline]
    readonly_fields = ['created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'address']
