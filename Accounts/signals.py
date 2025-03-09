from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivityLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        request_path="User Login",
        request_method="LOGIN",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        request_path="User Logout",
        request_method="LOGOUT",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
