from django.contrib import admin
from django.urls import path,include

import Manager.urls as MU
import Api.urls as APU

from Api.view_login import login as li,logout as lo,send_otp_login as so 

from Accounts.views import user_login,user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(MU)),
    path('api/', include(APU)),


    path("accounts/login/",  user_login, name="admin_login"),
    path("accounts/logout/", user_logout, name="admin_logout"),

    path("api/login/", li, name="api_login"),
    path("api/logout/", lo, name="api_logout"),
    path("api/send_otp_login/", so, name="api_send_otp"),


]
