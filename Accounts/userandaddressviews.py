from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount, Address
from .serializers import UserSerializer,AddressSerializer
from .decorators import token_auth_required
import json

@api_view(["GET", "POST"])
@token_auth_required
def user_profile_view(request):
    user = request.user
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        data.pop("email", None)  # Ensure email is not updated
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
@token_auth_required
def user_address_view(request):
    user = request.user
    if request.method == "GET":
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@token_auth_required
def address_detail_view(request, pk):
    user = request.user
    try:
        address = Address.objects.get(pk=pk, user=user)
    except Address.DoesNotExist:
        return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = AddressSerializer(address)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)