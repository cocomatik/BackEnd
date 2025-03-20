from django.db import models
from .models import POCOS


class FeatureProducts(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestSellers(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestOfSkinCare(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestOfImportedProducts(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestOfHairCare(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestOfFragrance(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestOfColorCosmetic(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)

class BestOfBodyCare(models.Model):
    pocos = models.ForeignKey(POCOS, on_delete=models.CASCADE)


from rest_framework import serializers
from .serializers import PocoListSerializer

class FeatureProductsSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = FeatureProducts
        fields = '__all__'

class BestSellersSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestSellers
        fields = '__all__'

class BestOfSkinCareSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestOfSkinCare
        fields = '__all__'

class BestOfImportedProductsSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestOfImportedProducts
        fields = '__all__'

class BestOfHairCareSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestOfHairCare
        fields = '__all__'

class BestOfFragranceSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestOfFragrance
        fields = '__all__'

class BestOfColorCosmeticSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestOfColorCosmetic
        fields = '__all__'

class BestOfBodyCareSerializer(serializers.ModelSerializer):
    pocos = PocoListSerializer()

    class Meta:
        model = BestOfBodyCare
        fields = '__all__'
