from rest_framework import serializers
from .models import Order, Cart, CartItem, OrderedCart, OrderedCartItem
from Accounts.models import Address, UserAccount
from Accounts.serializers import AddressSerializer, UserSerializer
from django.contrib.contenttypes.models import ContentType
from POCOS.models import POCOS
from POJOS.models import POJOS


class CartItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "sku", "product_details"]

    def get_product_details(self, obj):
        product_model = obj.product_type.model_class() if obj.product_type else None
        if product_model in [POCOS, POJOS]:
            product = product_model.objects.filter(sku=obj.sku).first()
            if product:
                return {
                    "sku": obj.sku,
                    "name": product.title,
                    "price": product.price,
                    "display_image": str(product.display_image),
                }
            else:
                return {
                    "sku": obj.sku,
                    "unavailable": True,
                    "message": "Product no longer available",
                    "price": None,
                    "display_image": None
                }
        return {"error": "Product not found"}


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cart_items", many=True)
    total_items = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "status", "items", "total_items", "total_value"]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_value(self, obj):
        total = 0
        for item in obj.cart_items.all():
            product_model = item.product_type.model_class() if item.product_type else None
            if product_model in [POCOS, POJOS]:
                product = product_model.objects.filter(sku=item.sku).first()
                if product:
                    total += item.quantity * product.price
        return total


class OrderedCartItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderedCartItem
        fields = ["sku", "quantity", "price_at_purchase", "product_details"]

    def get_product_details(self, obj):
        product_model = obj.product_type.model_class() if obj.product_type else None
        product = product_model.objects.filter(sku=obj.sku).first() if product_model else None
        if product:
            return {
                "name": product.title,
                "display_image": str(product.display_image) if product.display_image else None,
            }
        return {
            "name": None,
            "display_image": None,
        }


class OrderedCartSerializer(serializers.ModelSerializer):
    ordered_items = OrderedCartItemSerializer(many=True)

    class Meta:
        model = OrderedCart
        fields = ["total_value", "created_at", "ordered_items"]


class OrderSerializer(serializers.ModelSerializer):
    ordered_cart = OrderedCartSerializer()
    address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "payment_mode",
            "status",
            "created_at",
            "updated_at",
            "ordered_cart",
            "address",
            "user",
        ]
