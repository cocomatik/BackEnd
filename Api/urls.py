from django.urls import path,include
import POCOS.urls as PU
from .view_login import send_otp_login,login,logout

urlpatterns = [
    path('pocos/', include(PU)),


    
    path("login/", login, name="api_login"),
    path("logout/", logout, name="api_logout"),
    path("send_otp_login/", send_otp_login, name="api_send_otp"),
]