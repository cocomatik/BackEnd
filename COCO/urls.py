from django.contrib import admin
from django.urls import path,include

import Accounts.urls as ACU
import Manager.urls as MU
import Api.urls as APU

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(MU)),
    path('api/', include(APU)),
    path('accounts/', include(ACU)),
]
