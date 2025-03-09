from django.contrib import admin
from django.urls import path,include
import Accounts.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(Accounts.urls)),

]
