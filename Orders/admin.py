from django.contrib import admin
from .models import Cart,CartItem,Order
# from .models import Cart,CartItem
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)