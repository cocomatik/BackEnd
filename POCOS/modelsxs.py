from django.db import models
from .models import POCOS


class FeatureProducts(models.Model):
    objs = models.ManyToManyField(POCOS)  

class BestSellers(models.Model):
    objs = models.ManyToManyField(POCOS)  

class BestOfSkinCare(models.Model):
    objs = models.ManyToManyField(
        POCOS,
        limit_choices_to={'category': 'Skincare'}
    )

class BestOfImportedProducts(models.Model):
    objs = models.ManyToManyField(
        POCOS,
        limit_choices_to={'category': 'Imported Products'}
    )

class BestOfHairCare(models.Model):
    objs = models.ManyToManyField(
        POCOS,
        limit_choices_to={'category': 'Haircare'}
    )

class BestOfFragrance(models.Model):
    objs = models.ManyToManyField(
        POCOS,
        limit_choices_to={'category': 'Fragrances'}
    )

class BestOfColorCosmetic(models.Model):
    objs = models.ManyToManyField(
        POCOS,
        limit_choices_to={'category': 'Color Cosmetics'}
    )

class BestOfBodyCare(models.Model):
    objs = models.ManyToManyField(
        POCOS,
        limit_choices_to={'category': 'Bodycare'}
    )


from rest_framework import serializers
from .serializers import PocoListSerializer

class FeatureProductsSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = FeatureProducts
        fields = '__all__'

class BestSellersSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestSellers
        fields = '__all__'

class BestOfSkinCareSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestOfSkinCare
        fields = '__all__'

class BestOfImportedProductsSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestOfImportedProducts
        fields = '__all__'

class BestOfHairCareSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestOfHairCare
        fields = '__all__'

class BestOfFragranceSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestOfFragrance
        fields = '__all__'

class BestOfColorCosmeticSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestOfColorCosmetic
        fields = '__all__'

class BestOfBodyCareSerializer(serializers.ModelSerializer):
    objs = PocoListSerializer(many=True)

    class Meta:
        model = BestOfBodyCare
        fields = '__all__'
