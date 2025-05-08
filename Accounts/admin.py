from django.contrib import admin
from .models import UserAccount,Verification,Address,Wishlist
admin.site.register(UserAccount)
admin.site.register(Verification)
admin.site.register(Address)
admin.site.register(Wishlist)

