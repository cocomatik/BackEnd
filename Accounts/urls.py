from django.urls import path,include

from .views import user_login,user_logout
urlpatterns = [
    path("login/",  user_login, name="admin_login"),
    path("logout/", user_logout, name="admin_logout"),
]