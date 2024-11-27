from django.contrib import admin
from .models import Address, Order, OrderItem

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city', 'created')
    list_filter = ('created',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'created', 'updated', 'paid')
    list_filter = ('paid', 'created', 'updated')
    inlines = [OrderItemInline]