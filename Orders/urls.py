from django.urls import path
from .views import cart_view, add_to_cart,get_all_orders,get_order_details,update_cart_item,delete_cart_item,place_order,cancel_order
from .bills import generate_invoice
urlpatterns = [
    path("", get_all_orders, name="api-orders"),
    path("details/", get_order_details, name="api-order-details"),

    path("cart/", cart_view, name="cart"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("cart/update/", update_cart_item, name="update_cart"),
    path("cart/delete/", delete_cart_item, name="delete_cart"),
    path("place/", place_order, name="place_order"),
    path("cancel/", cancel_order, name="cancel_order"),
    path("invoice/<int:order_number>", generate_invoice, name="generate_invoice"),
]

