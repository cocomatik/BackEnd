from django.urls import path,include
import POCOS.urls as PU
from .view_login import send_otp_login,login,logout

urlpatterns = [
    path('pocos/', include(PU)),
]