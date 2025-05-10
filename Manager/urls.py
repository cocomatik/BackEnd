from django.urls import path
from Manager.views import bop,mbop,landing,dashboard, products, orders,add_product, edit_product,delete_product,best_of_products,order_detail,customers,customer_details,shipment_form,shipment_details
from Manager.delivery_views import create_shipment,pending_shipments,pending_SDetails

urlpatterns = [
    path('', landing, name='landing'),


    path('dashboard/', dashboard, name='dashboard'),


    path('products/', products, name='products'),
    path('products/add/', add_product, name='add_product'),
    path("products/edit/<str:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<str:product_id>/", delete_product, name="delete_product"),


    path('best-of-products/', best_of_products, name="best_of_products"),
    path('bop/',bop, name='handle_best_product'),
    path('mbop/',mbop, name='ad_best_product'),


    path("orders/", orders, name="order_list"),
    path('order/<str:order_number>/', order_detail, name='order_detail'),


    path('customers/',customers,name='customer_list'),
    path('customers/<int:customer_id>/', customer_details, name='customer_details'),

    path('shipment-form/<int:order_id>/', shipment_form, name='shipment_form'),
    path('create_shipment/', create_shipment, name='shipment_create'),
    path('shipments/', shipment_details, name='shipment_details'),
    path('shipments/pending/',pending_shipments,name='pending_shipments'),
    path('shipments/pending/<int:order_id>/',pending_SDetails,name='pending_SDetails'),

 
]