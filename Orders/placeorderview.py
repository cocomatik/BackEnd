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
from .models import OrderedCart, OrderedCartItem

# Initialize logger
logger = logging.getLogger(__name__)

def snapshot_cart_to_ordered(order):
    """
    Snapshot cart to ordered cart items after placing the order.
    """
    cart = order.cart
    ordered_cart = OrderedCart.objects.create(
        order=order,
        total_value=cart.value
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


@api_view(["POST"])
@token_auth_required
def place_order(request):
    """
    Place an order and integrate with Shiprocket for shipping.
    """
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    # Check if the cart has items
    if not cart.cart_items.exists():
        return Response({"error": "Cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

    # Get address and payment mode
    address_id = request.data.get("address_id")
    payment_mode = request.data.get("payment_mode")

    # Validate address and payment mode
    if not address_id or not payment_mode:
        return Response({"error": "Address ID and payment mode are required."}, status=status.HTTP_400_BAD_REQUEST)

    address = get_object_or_404(Address, id=address_id, user=user)

    if payment_mode not in ["paymentgateway", "cashondelivery"]:
        return Response({"error": "Invalid payment mode."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 🚀 Integrate with Shiprocket first before creating order
        shiprocket = ShiprocketAPI()
        shiprocket_response = shiprocket.create_order(cart)

        # Log Shiprocket response
        logger.info(f"Shiprocket Response for Cart {cart.id}: {shiprocket_response}")

        # Handle failure in Shiprocket integration
        if "error" in shiprocket_response:
            return Response({
                "message": "Order placement failed, failed to integrate with Shiprocket.",
                "shiprocket_error": shiprocket_response
            }, status=status.HTTP_206_PARTIAL_CONTENT)

        # If Shiprocket integration is successful, proceed with order creation
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                cart=cart, 
                user=user, 
                address=address, 
                payment_mode=payment_mode
            )

            # Snapshot the cart to ordered cart
            snapshot_cart_to_ordered(order)

            # Update cart status to 'ordered'
            cart.status = "ordered"
            cart.save()

            # Create a new pending cart for the user
            Cart.objects.create(user=user, status="pending")

    except Exception as e:
        logger.error(f"Order placement failed: {str(e)}")
        return Response({"error": "An error occurred while placing the order."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Successful order placement
    return Response({
        "message": "Order placed successfully.",
        "order_id": order.id,
        "shiprocket_response": shiprocket_response
    }, status=status.HTTP_201_CREATED)
