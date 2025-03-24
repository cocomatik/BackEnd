from .models import Address,UserAccount
from rest_framework import serializers 

class AddressSerializer(serializers.ModelSerializer):
    """Serializes address details"""
    class Meta:
        model = Address
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    """Serializes user details"""
    class Meta:
        model = UserAccount
        fields = ["id", "name", "email"]