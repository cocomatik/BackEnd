from django.urls import path
from Manager.views import bop,dbop,abop,landing,dashboard, products, orders,add_product, edit_product,delete_product,best_of_products

# order_detail,order_edit,order_delete


urlpatterns = [
    path('', landing, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', products, name='products'),
    path('products/add/', add_product, name='add_product'),
    path("products/edit/<str:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<str:product_id>/", delete_product, name="delete_product"),
    path('best-of-products/', best_of_products, name="best_of_products"),
    path('bop/',bop, name='handle_best_product'),
    path('dbop/',dbop, name='df_best_product'),
    path('abop/',abop, name='ad_best_product'),

    path("orders/", orders, name="order_list"),
    # path('order/<int:order_id>/', order_detail, name='order_detail'),  # View order details
    # path('order/<int:order_id>/edit/', order_edit, name='order_edit'),  # Edit order
    # path('order/<int:order_id>/delete/', order_delete, name='order_delete'),
]
