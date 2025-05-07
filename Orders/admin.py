from django.contrib import admin
from .models import Cart,CartItem,Order,Wishlist
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)

from .models import OrderHistory, OrderHistoryItem

class OrderHistoryItemInline(admin.TabularInline):
    model = OrderHistoryItem
    extra = 0

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'payment_mode', 'status', 
        'sub_total', 'shipping_charges', 
        'packaging_charges', 'cod_charges', 'handling_charges',
        'created_at'
    ]
    list_filter = ['payment_mode', 'status', 'created_at']
    search_fields = ['order_number', 'user__email']
    inlines = [OrderHistoryItemInline]
    readonly_fields = [
        'order', 'user', 'address', 'order_number', 'payment_mode', 
        'status', 'sub_total', 'discount', 'tax', 
        'shipping_charges', 'additional_charges',
        'packaging_charges', 'cod_charges', 'handling_charges',
        'length', 'breadth', 'height', 'weight',
        'reseller_name', 'company_name', 'shiprocket_order_id', 
        'created_at'
    ]