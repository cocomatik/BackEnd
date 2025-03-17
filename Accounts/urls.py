from django.urls import path,include

from .views import user_login,user_logout
urlpatterns = [
    path("accounts/login/",  user_login, name="admin_login"),
    path("accounts/logout/", user_logout, name="admin_logout"),
]