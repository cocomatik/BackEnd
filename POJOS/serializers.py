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
        fields = '__all__'

    def get_discount(self, obj):
        """Ensure discount is serialized correctly."""
        return obj.discount


class PojoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra images of POJOS."""
    class Meta:
        model = PojoImage
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'pojo', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'pojo', 'created_at']


class PojoDetailSerializer(serializers.ModelSerializer):
    extra_images = PojoImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = POJOS
        fields = [
            'sku', 'title', 'description', 'price', 'mrp', 'stock',
            'category', 'brand', 'display_image', 'rating', 'size',
            'created_at', 'updated_at', 'extra_images', 'reviews', 'discount'
        ]

    def get_discount(self, obj):
        return obj.discount or 0
