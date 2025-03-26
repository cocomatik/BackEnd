from rest_framework import serializers
from .models import POJOS, PojoImage, Review, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    class Meta:
        model = Category
        fields = "__all__"


class PojoListSerializer(serializers.ModelSerializer):
    """Serializer for listing POJOS."""
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POJOS
        fields = ["sku", "title","description", "size", "mrp", "price", "discount", "stock", "category", "brand", "display_image", "rating"]

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount


class PojoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra images of POJOS."""
    class Meta:
        model = PojoImage
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""
    class Meta:
        model = Review
        fields = ['user_name', "verified_user", 'rating', 'comment', 'created_at']


class PojoDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed POJOS view."""
    extra_images = PojoImageSerializer(many=True, read_only=True, source="pojoimage_set")
    reviews = ReviewSerializer(many=True, read_only=True, source="review_set")
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POJOS
        fields = ['sku', 'title', 'description', "mrp", 'price', "discount", 'stock', 'rating', 'display_image', 'extra_images', 'reviews']

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount
