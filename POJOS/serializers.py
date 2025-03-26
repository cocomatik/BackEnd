from rest_framework import serializers
from .models import POJOS, PojoImage, Review

class PojoListSerializer(serializers.ModelSerializer):
    """Serializer for the pojo list API."""
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POJOS
        fields = ["pojo_id", "sku", "title", "size", "mrp", "price", "discount", "stock", "category", "brand", "display_image", "rating"]

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount


class PojoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra pojo images."""
    class Meta:
        model = PojoImage
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for pojo reviews."""
    class Meta:
        model = Review
        fields = ['user_name', "verified_user", 'rating', 'comment', 'created_at']


class PojoDetailSerializer(serializers.ModelSerializer):
    """Serializer for the pojo detail API."""
    extra_images = PojoImageSerializer(many=True, read_only=True, source="pojoimage_set")
    reviews = ReviewSerializer(many=True, read_only=True, source="review_set")
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POJOS
        fields = ['pojo_id', 'sku', 'title', 'description', "mrp", 'price', "discount", 'stock', 'rating', 'display_image', 'extra_images', 'reviews']

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount
