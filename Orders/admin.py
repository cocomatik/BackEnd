from django.contrib import admin
from .models import Cart,CartItem,Order,OrderedCart,OrderedCartItem
# from .models import Cart,CartItem
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderedCart)
admin.site.register(OrderedCartItem)