from django.urls import path
from Manager.views import dashboard, products, orders, customers, reports, settings, logout_view, add_product


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('products/', products, name='products'),
    path('products/add/', add_product, name='add_product'),
    # path('products/edit/<int:id>/', edit_product, name='edit_product'),
    # path('products/delete/<int:id>/', delete_product, name='delete_product'),
    path('orders/', orders, name='orders'),
    path('customers/', customers, name='customers'),
    path('reports/', reports, name='reports'),
    path('settings/', settings, name='settings'),
    path('logout/', logout_view, name='logout'),
]
