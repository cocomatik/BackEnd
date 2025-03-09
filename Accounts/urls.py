from django.urls import path,include
from Accounts import urls as A_URLS

from .views import login,logout,send_otp_login

urlpatterns = [
    path('send_otp_login/',send_otp_login),
    path('login/',login),
    path('logout/',logout),
]
