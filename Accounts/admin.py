from django.contrib import admin
from .models import UserAccount,Verification,Address
admin.site.register(UserAccount)
admin.site.register(Verification)
admin.site.register(Address)

