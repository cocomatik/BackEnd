from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from Accounts.decorators import token_auth_required
from Accounts.models import Address
from POCOS.models import POCOS
from POJOS.models import POJOS
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer


@api_view(["GET"])
@token_auth_required
def cart_view(request):
    """
    Fetch the user's cart with all items, total item count, and total cart value.
    """
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, status="pending")
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
    """
    user = request.user
    cart = get_object_or_404(Cart, user=user, status="pending")

    cart_item_id = request.data.get("cart_item_id")

    if not cart_item_id:
        return Response({"error": "'cart_item_id' is required."}, status=status.HTTP_400_BAD_REQUEST)

    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    cart_item.delete()

    return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@token_auth_required
def get_orders(request):
    """
    Fetch all orders placed by the user.
    """
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@token_auth_required
def get_order_details(request, order_id):
    """
    Fetch details of a specific order by its ID.
    """
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=user)

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)