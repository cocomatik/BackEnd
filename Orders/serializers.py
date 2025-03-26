from rest_framework import serializers
from .models import Order, Cart, CartItem
from Accounts.models import Address, UserAccount  
from Accounts.serializers import AddressSerializer, UserSerializer  
from django.contrib.contenttypes.models import ContentType
from POCOS.models import POCOS
from POJOS.models import POJOS

class CartItemSerializer(serializers.ModelSerializer):
    """Serializes cart items with product details"""
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "sku", "product_details"]

    def get_product_details(self, obj):
        """Retrieve product details using SKU"""
        product_model = obj.product_type.model_class()  # Get the model class
        product = product_model.objects.filter(sku=obj.sku).first()  

        if product:
            return {
                "sku": obj.sku,
                "name": product.title,
                "price": product.price
            }
        return {"error": "Product not found"}

class CartSerializer(serializers.ModelSerializer):
    """Serializes the cart with items and calculates total values"""
    items = CartItemSerializer(source="cart_items", many=True)
    total_items = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "status", "items", "total_items", "total_value"]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_value(self, obj):
        return sum(
            item.quantity * item.product.price 
            for item in obj.cart_items.all() if item.product
        )

class OrderSerializer(serializers.ModelSerializer):
    """Serializes the order with full details"""
    cart = CartSerializer()  # Nest the full cart details
    address = AddressSerializer()  # Include address details
    user = UserSerializer()  # Include user details

    class Meta:
        model = Order
        fields = ["id", "payment_mode", "created_at", "updated_at", "cart", "address", "user"]
