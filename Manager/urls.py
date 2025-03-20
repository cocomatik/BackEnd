from django.urls import path
from Manager.views import landing,dashboard, products, orders,add_product, edit_product,delete_product


urlpatterns = [
    path('', landing, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', products, name='products'),
    path('products/add/', add_product, name='add_product'),
    path("products/edit/<str:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<str:product_id>/", delete_product, name="delete_product"),
    path('orders/', orders, name='orders'),
]
