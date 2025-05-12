from .models import Address,UserAccount,Wishlist
from rest_framework import serializers 
from POCOS.models import POCOS
from POJOS.models import POJOS


class AddressSerializer(serializers.ModelSerializer):
    """Serializes address details"""
    class Meta:
        model = Address
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    """Serializes user details"""
    class Meta:
        model = UserAccount
        fields = ["id", "first_name","last_name", "email","phone","age","gender"]



class WishListSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = ["id", "sku", "product_type", "product_details"]

    def get_product_details(self, obj):
        product_model = obj.product_type.model_class() if obj.product_type else None
        if product_model in [POCOS, POJOS]:
            product = product_model.objects.filter(sku=obj.sku).first()
            if product:
                return {
                    "sku": obj.sku,
                    "name": product.title,
                    "price": product.price,
                    "mrp": product.mrp,
                    "description": product.description,
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
