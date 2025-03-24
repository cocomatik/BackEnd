from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
from .utils.shiprocket import ShiprocketAPI
from Accounts.decorators import token_auth_required
from Accounts.models import Address
from .models import Cart, Order

@api_view(["POST"])
@token_auth_required
def place_order(request):
    """
    Place an order and integrate with Shiprocket for shipping.
    """
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")
    address_id = request.data.get("address_id")
    payment_mode = request.data.get("payment_mode")

    if not address_id or not payment_mode:
        return Response({"error": "Address ID and payment mode are required."}, status=status.HTTP_400_BAD_REQUEST)

    address = get_object_or_404(Address, id=address_id, user=user)

    if payment_mode not in ["paymentgateway", "cashondelivery"]:
        return Response({"error": "Invalid payment mode."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        order = Order.objects.create(cart=cart, user=user, address=address, payment_mode=payment_mode)

        # Update cart status
        cart.status = "ordered"
        cart.save()

        # Create a new empty cart for the user
        Cart.objects.create(user=user, status="pending")

        # 🚀 Integrate Shiprocket
        shiprocket = ShiprocketAPI()
        shiprocket_response = shiprocket.create_order(order)

    return Response({
        "message": "Order placed successfully.",
        "order_id": order.id,
        "shiprocket_response": shiprocket_response
    }, status=status.HTTP_201_CREATED)
