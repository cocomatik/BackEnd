from django.urls import path
from Manager.views import bop,dbop,abop,landing,dashboard, products, orders,add_product, edit_product,delete_product,best_of_products,order_detail,delete_order,delete_cart_item,edit_order,customers,customer_details


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
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path("order/<int:order_id>/delete/", delete_order, name="delete_order"),
    path("cart-item/<int:item_id>/delete/", delete_cart_item, name="delete_cart_item"),
    path("order/<int:order_id>/edit/", edit_order, name="edit_order"),

    path('customers/',customers,name='customer_list'),
    path('customers/<int:customer_id>/', customer_details, name='customer_details'),

 
]