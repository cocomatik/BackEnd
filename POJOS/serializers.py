from rest_framework import serializers
from .models import POJOS, PojoImage, Review


class PojoListSerializer(serializers.ModelSerializer):
    """Serializer for the pojo list API."""
    class Meta:
        model = POJOS
        fields = ["pojo_id","title","size","mrp","price","discount","stock","category","brand","display_image","rating"]

class PojoImageSerializer(serializers.ModelSerializer):
    """Serializer for extra pojo images."""
    class Meta:
        model = PojoImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for pojo reviews."""
    class Meta:
        model = Review
        fields = ['user_name',"verified_user", 'rating', 'comment', 'created_at']


class PojoDetailSerializer(serializers.ModelSerializer):
    """Serializer for the pojo detail API."""
    extra_images = PojoImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = POJOS
        fields = ['pojo_id', 'title', 'description',"mrp",'price',"discount", 'stock', 'rating', 'display_image', 'extra_images', 'reviews']
