from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserAccount, Address,Wishlist
from .serializers import UserSerializer,AddressSerializer
from .decorators import token_auth_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer,WishListSerializer
from POCOS.models import POCOS
from POJOS.models import POJOS
from django.contrib.contenttypes.models import ContentType

@api_view(["GET", "PUT"])
@token_auth_required
def user_profile_view(request):
    user = request.user

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data.copy()
        data.pop("email", None)  # Prevent updating email
        serializer = UserSerializer(user, data=data, partial=True)  # partial=True allows partial update
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
        data = request.data.copy()
        data['user'] = user.id 
        print(data)
        serializer = AddressSerializer(data=data)
        print(serializer)
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
    


@api_view(["GET", "POST", "DELETE"])
@token_auth_required
def wishlist_view(request):
    user = request.user

    if request.method == "GET":
        wishlist_items = Wishlist.objects.filter(user=user)
        serializer = WishListSerializer(wishlist_items, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        sku = request.data.get("sku")
        if not sku:
            return Response({"error": "Each product must have 'sku'."}, status=status.HTTP_400_BAD_REQUEST)

        sku_prefix = sku.split("-")[0].upper()
        if sku_prefix == "POCO":
            product_model = POCOS
        elif sku_prefix == "POJO":
            product_model = POJOS
        else:
            return Response({"error": f"Unknown SKU prefix '{sku_prefix}' in '{sku}'."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(product_model, sku=sku)
        content_type = ContentType.objects.get_for_model(product_model)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            sku=sku,
            product_type=content_type,
        )

        serializer = WishListSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    elif request.method == "DELETE":
        sku = request.data.get("sku")
        if not sku:
            return Response({"error": "Please provide SKU to delete."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wishlist_item = Wishlist.objects.get(user=user, sku=sku)
            wishlist_item.delete()
            return Response({"message": f"Item with SKU '{sku}' removed from wishlist."}, status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response({"error": f"No wishlist item found with SKU '{sku}'."}, status=status.HTTP_404_NOT_FOUND)
