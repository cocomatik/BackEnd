from django.contrib import admin
from django.urls import path,include
import Accounts.urls as AU
import Manager.urls as MU
import Api.urls as APU

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(MU)),
    path('accounts/', include(AU)),
    path('api/', include(APU)),
]
