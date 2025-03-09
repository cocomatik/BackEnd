from django.contrib import admin
from .models import UserAccount,Verification
admin.site.register(UserAccount)
admin.site.register(Verification)

from .models import UserActivityLog

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_path', 'ip_address', 'timestamp')
    search_fields = ('user__name', 'request_path', 'ip_address')
    list_filter = ('timestamp',)
