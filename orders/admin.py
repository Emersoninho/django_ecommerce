from django.contrib import admin
from .models import Address, Order, OrderItem

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city', 'created')
    list_filter = ('created',)
    search_fields = ('first_name', 'last_name', 'email', 'address_line', 'city')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_address', 'created', 'updated', 'paid', 'get_total_cost')
    list_filter = ('paid', 'created', 'updated')
    search_fields = ('address__first_name', 'address__last_name', 'address__email')
    inlines = [OrderItemInline]

    def get_full_address(self, obj):
        """
        Método para retornar o endereço completo a partir do modelo Address.
        """
        if obj.address:
            return f"{obj.address.first_name} {obj.address.last_name}, {obj.address.address_line}, {obj.address.city}, {obj.address.state} - {obj.address.zipcode}"
        return "Endereço não definido"
    get_full_address.short_description = "Endereço Completo"

    def get_total_cost(self, obj):
        """
        Método para calcular e exibir o total do pedido no admin.
        """
        total_cost = sum(item.price * item.quantity for item in obj.items.all()) + obj.shipping_cost
        return f"R$ {total_cost:.2f}"
    get_total_cost.short_description = "Total"
