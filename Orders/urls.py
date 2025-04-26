from django.urls import path
from .views import cart_view, add_to_cart,get_pending_orders,processed_orders,get_order_details,update_cart_item,delete_cart_item,place_order
from .bills import generate_invoice
urlpatterns = [
    path("", processed_orders, name="api-orders"),
    path("pending/", get_pending_orders, name="api-orders-pending"),
    path("o/<int:order_id>/", get_order_details, name="api-order-details"),
    path("cart/", cart_view, name="cart"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("cart/update/", update_cart_item, name="update_cart"),
    path("cart/delete/", delete_cart_item, name="delete_cart"),
    path("place/", place_order, name="checkout_cart"),
    path("invoice/<int:order_number>", generate_invoice, name="generate_invoice"),
]

