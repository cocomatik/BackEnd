from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import AccountManager

from django.utils.timezone import now
from datetime import timedelta


class UserAccount(AbstractBaseUser, PermissionsMixin):  
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email' 

    def __str__(self):
        return self.email
    

class Verification(models.Model):
    email = models.EmailField(unique=True,blank=False,null=False)
    otp = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return now() < self.updated_at + timedelta(minutes=5000000)

    # def set_otp(self, otp):
    #     self.otp = make_password(otp)

    def check_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return f"OTP for {self.email} is {self.otp}"
        


# from django.db import models
# from django.utils.timezone import now


# class UserActivityLog(models.Model):
#     user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
#     request_path = models.CharField(max_length=255)  # Store the path of the request
#     request_method = models.CharField(max_length=10)  # GET, POST, etc.
#     ip_address = models.GenericIPAddressField(null=True, blank=True)  # User's IP
#     user_agent = models.TextField(null=True, blank=True)  # Browser or client information
#     timestamp = models.DateTimeField(default=now)  # Log time
#     additional_info = models.JSONField(null=True, blank=True)  # For extra context

#     def __str__(self):
#         return f"Log for {self.user.name if self.user else 'Anonymous'} on {self.timestamp}"
