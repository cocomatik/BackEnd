from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import AccountManager

from django.utils.timezone import now
from datetime import timedelta


class UserAccount(AbstractBaseUser, PermissionsMixin):  
    name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    email = models.EmailField(unique=True)  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email' 

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15) 
    house_no = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    locality = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    district = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    pincode = models.CharField(max_length=10)  

    def __str__(self):
        return str(f"{self.user}- Adrs {self.id}")    

class Verification(models.Model):
    email = models.EmailField(unique=True,blank=False,null=False)
    otp = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return now() < self.updated_at + timedelta(minutes=5000000)

    def check_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return f"OTP for {self.email} is {self.otp}"
        
