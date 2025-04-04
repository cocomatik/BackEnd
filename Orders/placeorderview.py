from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
import logging
from .utils.shiprocket import ShiprocketAPI
from Accounts.decorators import token_auth_required
from Accounts.models import Address
from .models import Cart, CartItem, Order

# Initialize logger
logger = logging.getLogger(__name__)

@api_view(["POST"])
@token_auth_required
def place_order(request):
    """
    Place an order and integrate with Shiprocket for shipping.
    """
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    if not cart.cart_items.exists():
        return Response({"error": "Cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

    address_id = request.data.get("address_id")
    payment_mode = request.data.get("payment_mode")

    if not address_id or not payment_mode:
        return Response({"error": "Address ID and payment mode are required."}, status=status.HTTP_400_BAD_REQUEST)

    address = get_object_or_404(Address, id=address_id, user=user)

    if payment_mode not in ["paymentgateway", "cashondelivery"]:
        return Response({"error": "Invalid payment mode."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Create order
            order = Order.objects.create(cart=cart, user=user, address=address, payment_mode=payment_mode)

            # Update cart status
            cart.status = "ordered"
            cart.save()

            # Create a new empty cart for the user
            Cart.objects.create(user=user, status="pending")

            # 🚀 Integrate Shiprocket
            shiprocket = ShiprocketAPI()
            shiprocket_response = shiprocket.create_order(order)

            # Log the Shiprocket response
            logger.info(f"Shiprocket Response for Order {order.id}: {shiprocket_response}")

            # Handle Shiprocket failures
            if "error" in shiprocket_response:
                return Response({
                    "message": "Order placed, but failed to integrate with Shiprocket.",
                    "order_id": order.id,
                    "shiprocket_error": shiprocket_response
                }, status=status.HTTP_206_PARTIAL_CONTENT)

    except Exception as e:
        logger.error(f"Order placement failed: {str(e)}")
        return Response({"error": "An error occurred while placing the order."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "message": "Order placed successfully.",
        "order_id": order.id,
        "shiprocket_response": shiprocket_response
    }, status=status.HTTP_201_CREATED)
