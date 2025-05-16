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
        fields = '__all__'

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount

class PocoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra images of POCOS."""
    class Meta:
        model = PocoImage
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'poco', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'poco', 'created_at']


class PocoDetailSerializer(serializers.ModelSerializer):
    extra_images = PocoImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POCOS
        fields = [
            'sku', 'title', 'description', 'price', 'mrp', 'stock',
            'category', 'brand', 'display_image', 'rating', 'size',
            'created_at', 'updated_at', 'extra_images', 'reviews', 'discount'
        ]

    def get_discount(self, obj):
        return obj.discount or 0


