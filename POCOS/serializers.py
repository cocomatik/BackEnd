from rest_framework import serializers
from .models import POCOS, PocoImage, Review


class PocoListSerializer(serializers.ModelSerializer):
    """Serializer for the poco list API."""
    class Meta:
        model = POCOS
        fields = ["poco_id","title","size","price","stock","category","brand","display_image","rating"]

class PocoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra poco images."""
    class Meta:
        model = PocoImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for poco reviews."""
    class Meta:
        model = Review
        fields = ['user_name',"verified_user", 'rating', 'comment', 'created_at']


class PocoDetailSerializer(serializers.ModelSerializer):
    """Serializer for the poco detail API."""
    extra_images = PocoImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = POCOS
        fields = ['poco_id', 'title', 'description', 'price', 'stock', 'rating', 'display_image', 'extra_images', 'reviews']
