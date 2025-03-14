from django.contrib import admin
from django.urls import path,include

from .views import dashboard

urlpatterns = [
    path('',dashboard,name="DASHBOARD"),
]