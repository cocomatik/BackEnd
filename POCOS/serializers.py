from rest_framework import serializers
from .models import POCOS, PocoImage, Review, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    class Meta:
        model = Category
        fields = "__all__"

class PocoListSerializer(serializers.ModelSerializer):
    """Serializer for listing POCOS."""
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POCOS
        fields = ["sku", "title", "size", "mrp", "price", "discount", "stock", "category", "brand", "display_image", "rating"]

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount

class PocoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra images of POCOS."""
    class Meta:
        model = PocoImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""
    class Meta:
        model = Review
        fields = ['user_name', "verified_user", 'rating', 'comment', 'created_at']

class PocoDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed POCOS view."""
    extra_images = PocoImageSerializer(many=True, read_only=True, source="pocoimage_set")
    reviews = ReviewSerializer(many=True, read_only=True, source="review_set")
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POCOS
        fields = ['sku', 'title', 'description', "mrp", 'price', "discount", 'stock', 'rating', 'display_image', 'extra_images', 'reviews']

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount
