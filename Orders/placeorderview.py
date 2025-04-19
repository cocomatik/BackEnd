from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
import logging
from Delivery.shiprocket import ShiprocketAPI
from Accounts.decorators import token_auth_required
from Accounts.models import Address
from .models import Cart, CartItem, Order
from .models import OrderedCart, OrderedCartItem

# Initialize logger
logger = logging.getLogger(__name__)

def snapshot_cart_to_ordered(cart, order, status="FAIL", remark=""):
    ordered_cart = OrderedCart.objects.create(
        order=order,
        total_value=cart.value,
        status=status,
        remark=remark
    )

    for item in cart.cart_items.all():
        product_model = item.product_type.model_class() if item.product_type else None
        product = product_model.objects.filter(sku=item.sku).first() if product_model else None

        OrderedCartItem.objects.create(
            ordered_cart=ordered_cart,
            sku=item.sku,
            product_type=item.product_type,
            quantity=item.quantity,
            price_at_purchase=product.price if product else 0
        )

    return ordered_cart

@api_view(["POST"])
@token_auth_required
def place_order(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    if not cart.cart_items.exists():
        return Response({"error": "Cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

    address_id = request.data.get("address_id")
    payment_mode = request.data.get("payment_mode")
    payment_value = request.data.get("payment_value")

    if not address_id or not payment_mode:
        return Response({"error": "Address ID and payment mode are required."}, status=status.HTTP_400_BAD_REQUEST)

    if payment_mode not in ["PG", "COD"]:
        return Response({"error": "Invalid payment mode."}, status=status.HTTP_400_BAD_REQUEST)

    address = get_object_or_404(Address, id=address_id, user=user)

    try:
        with transaction.atomic():
            order, created = Order.objects.get_or_create(
                cart=cart,
                user=user,
                address=address,
                payment_mode=payment_mode,
                total_price=payment_value
            )

            # Default snapshot with FAIL first
            ordered_cart = snapshot_cart_to_ordered(cart, order)

        shiprocket = ShiprocketAPI()
        shiprocket_response = shiprocket.create_order(order=order)

        logger.info(f"Shiprocket Response for Order {order.order_number}: {shiprocket_response}")

        if "error" in shiprocket_response:
            ordered_cart.status = "FAIL"
            ordered_cart.remark = str(shiprocket_response.get("message", "Shiprocket error"))
            ordered_cart.save()
            return Response({
                "message": "Order created, but failed to integrate with Shiprocket.",
                "order_id": order.order_number,
                "shiprocket_error": shiprocket_response
            }, status=status.HTTP_206_PARTIAL_CONTENT)

        # Success flow
        cart.status = "ORDERED"
        cart.save()

        order.status = "PROCESSING"
        order.save()

        ordered_cart.status = "SUCCESS"
        ordered_cart.shiprocket_order_id = shiprocket_response.get("order_id", "")
        ordered_cart.remark = "Shiprocket order placed successfully"
        ordered_cart.save()

        # New cart for the user
        Cart.objects.create(user=user, status="pending")

    except Exception as e:
        logger.error(f"Order or Shiprocket integration failed: {str(e)}")
        return Response({
            "error": "Something went wrong during order placement.",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "message": "Order placed successfully and integrated with Shiprocket.",
        "order_id": order.order_number,
        "shiprocket_response": shiprocket_response
    }, status=status.HTTP_201_CREATED)
