from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from Accounts.decorators import token_auth_required
from Accounts.models import Address
from POCOS.models import POCOS
from POJOS.models import POJOS
from .models import Cart, CartItem, Order ,OrderHistory,OrderHistoryItem
from .serializers import CartSerializer, CartItemSerializer, ActiveOrderSerializer,ArchivedOrderSerializer,OrderHistorySerializer
from django.db import transaction
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import logging
from decimal import Decimal

from Payments.utils import initiate_phonepe_payment 
# Initialize logger
logger = logging.getLogger(__name__)


    
@api_view(["GET"])
@token_auth_required
def cart_view(request):
    """
    Fetch the user's cart with all items, total item count, and total cart value.
    Handles empty cart scenario.
    """
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, status="pending")

    if not cart.cart_items.exists():
        return Response({"message": "Your cart is empty."}, status=status.HTTP_200_OK)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@token_auth_required
def add_to_cart(request):
    """
    Add multiple products to the cart in a single request.
    Determines product type based on SKU prefix.
    """
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, status="pending")

    products = request.data.get("products")  # Expecting a list of {sku, quantity}

    if not products or not isinstance(products, list):
        return Response({"error": "Invalid or missing 'products' list."}, status=status.HTTP_400_BAD_REQUEST)

    added_items = []

    for product_data in products:
        sku = product_data.get("sku")
        quantity = int(product_data.get("quantity", 1))

        if not sku:
            return Response({"error": "Each product must have 'sku'."}, status=status.HTTP_400_BAD_REQUEST)

        sku_prefix = sku.split("-")[0].upper()

        # Determine product model based on SKU prefix
        if sku_prefix == "POCO":
            product_model = POCOS
            product_type = "pocos"
        elif sku_prefix == "POJO":
            product_model = POJOS
            product_type = "pojos"
        else:
            return Response({"error": f"Unknown SKU prefix '{sku_prefix}' in '{sku}'."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(product_model, sku=sku)
        content_type = ContentType.objects.get_for_model(product_model)

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_type=content_type,
            sku=sku,
            title=product.title,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        added_items.append({
            "sku": sku,
            "product_type": product_type,
            "quantity": cart_item.quantity,
        })

    return Response({"message": "Products added to cart successfully.", "items": added_items}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
@token_auth_required
def update_cart_item(request):
    """
    Update quantity of an item in the cart.
    Handles invalid cart item and quantity.
    """
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    cart_item_id = request.data.get("cart_item_id")
    quantity = int(request.data.get("quantity", 1))

    if not cart_item_id or quantity <= 0:
        return Response({"error": "Valid 'cart_item_id' and 'quantity' are required."}, status=status.HTTP_400_BAD_REQUEST)

    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    cart_item.quantity = quantity
    cart_item.save()

    return Response({"message": "Cart item updated successfully."}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@token_auth_required
def delete_cart_item(request):
    """
    Remove an item from the cart.
    Handles cart item removal errors.
    """
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    cart_item_id = request.data.get("cart_item_id")

    if not cart_item_id:
        return Response({"error": "'cart_item_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    cart_item.delete()

    return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)



@api_view(["POST"])
@token_auth_required
def place_order(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    if not cart.cart_items.exists():
        return Response({"error": "Cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

    address_id = request.data.get("address_id")
    payment_mode = request.data.get("payment_mode")
    
    discount = Decimal(request.data.get('discount', 0))
    tax = Decimal(request.data.get('tax', 0))
    shipping_charges = Decimal(request.data.get('shipping_charges', 0))
    packaging_charges = Decimal(request.data.get('packaging_charges', 0))
    cod_charges = Decimal(request.data.get('cod_charges', 0))
    handling_charges = Decimal(request.data.get('handling_charges', 0))

    sub_total = cart.value  
    total_price = (sub_total + tax + shipping_charges + packaging_charges + cod_charges + handling_charges) - discount

    if not address_id or not payment_mode:
        return Response({"error": "Address ID and payment mode are required."}, status=status.HTTP_400_BAD_REQUEST)

    if payment_mode not in ["PG", "COD"]:
        return Response({"error": "Invalid payment mode."}, status=status.HTTP_400_BAD_REQUEST)

    address = get_object_or_404(Address, id=address_id, user=user)

    try:
        with transaction.atomic():
            order = Order.objects.create(
                cart=cart,
                user=user,
                rcv_address_name=address.address_name,
                rcv_address_type=address.address_type,
                rcv_name=address.name,
                rcv_contact_no=address.contact_no, 
                rcv_house_no=address.house_no,
                rcv_street=address.street,
                rcv_locality=address.locality,
                rcv_city=address.city,
                rcv_district=address.district,
                rcv_state=address.state,
                rcv_pincode=address.pincode,
                payment_mode=payment_mode,
                discount=discount,
                tax=tax,
                shipping_charges=shipping_charges,
                packaging_charges=packaging_charges,
                cod_charges=cod_charges,
                handling_charges=handling_charges,
                sub_total=sub_total,
                total_price=total_price,
                status= "ORDERED"
            )

            order.save()
            cart.status = "ORDERED"
            cart.save()

            # Handle PG (PhonePe)
            if payment_mode == "PG":
                payment_data = initiate_phonepe_payment(order)
                return Response({
                    "message": "Redirect to PhonePe to complete payment.",
                    "order_id": order.order_number,
                    "payment_url": payment_data.get("redirect_url")
                }, status=status.HTTP_202_ACCEPTED)

            # COD Success
            return Response({
                "message": "Order placed successfully with COD.",
                "order_id": order.order_number
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Order placement failed: {str(e)}")
        return Response({
            "error": "Something went wrong during order placement.",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@token_auth_required
def cancel_order(request):
    user = request.user
    order_number = request.data.get("order_number")

    if not order_number:
        return Response({"error": "Order number is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(order_number=order_number, user=user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Example condition: allow cancellation within 30 minutes of creation
    time_limit = order.created_at + timedelta(minutes=120)
    if timezone.now() > time_limit:
        return Response({"error": "Order can no longer be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

    if order.status == "cancelled":
        return Response({"message": "Order is already cancelled."}, status=status.HTTP_200_OK)

    # Perform cancellation
    order.status = "cancelled"
    order.save()

    return Response({"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)


@api_view(["GET"])
@token_auth_required
def get_all_orders(request):
    pending_orders = Order.objects.filter(user=request.user, status="ORDERED").order_by("-created_at")
    processed_orders = OrderHistory.objects.filter(user=request.user).order_by("-created_at")

    response_data = {
        "pending": ActiveOrderSerializer(pending_orders, many=True).data,
        "processed": OrderHistorySerializer(processed_orders, many=True).data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@token_auth_required
def get_order_details(request):

    user = request.user
    try:
        order_number=request.data.get("order_number")
        order = get_object_or_404(Order, order_number=order_number, user=user)
        serializer = ActiveOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except :
        return Response({"message":"Could not find the order details."})