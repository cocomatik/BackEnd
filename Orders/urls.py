from django.urls import path
from .views import cart_view, add_to_cart,get_orders,get_order_details,update_cart_item
from .placeorderview import place_order
urlpatterns = [
    path("", get_orders, name="orders"),
    path("o/<int:order_id>/", get_order_details, name="order-details"),
    path("cart/", cart_view, name="cart"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("cart/update/", update_cart_item, name="update_cart"),
    path("place/", place_order, name="checkout_cart"),
]
