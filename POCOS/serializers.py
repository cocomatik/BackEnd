from rest_framework import serializers
from .models import POCOS, PocoImage, Review

class PocoListSerializer(serializers.ModelSerializer):
    """Serializer for the poco list API."""
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POCOS
        fields = ["poco_id", "sku", "title", "size", "mrp", "price", "discount", "stock", "category", "brand", "display_image", "rating"]

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount


class PocoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra poco images."""
    class Meta:
        model = PocoImage
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for poco reviews."""
    class Meta:
        model = Review
        fields = ['user_name', "verified_user", 'rating', 'comment', 'created_at']


class PocoDetailSerializer(serializers.ModelSerializer):
    """Serializer for the poco detail API."""
    extra_images = PocoImageSerializer(many=True, read_only=True, source="pocoimage_set")
    reviews = ReviewSerializer(many=True, read_only=True, source="review_set")
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POCOS
        fields = ['poco_id', 'sku', 'title', 'description', "mrp", 'price', "discount", 'stock', 'rating', 'display_image', 'extra_images', 'reviews']

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount
