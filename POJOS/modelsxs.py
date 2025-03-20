from django.db import models
from .models import POJOS

from rest_framework import serializers
from .serializers import PojoListSerializer

class FeatureProducts(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestSellers(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfWeddingJewellery(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)


class BestOfWeddingJewellerySerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfWeddingJewellery
        fields = '__all__'

class BestOfPendants(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfPendantsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfPendants
        fields = '__all__'

class BestOfNoseRings(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfNoseRingsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfNoseRings
        fields = '__all__'

class BestOfNecklace(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)


class BestOfNecklaceSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfNecklace
        fields = '__all__'

class BestOfOneGramGoldenJewellery(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfOneGramGoldenJewellerySerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfOneGramGoldenJewellery
        fields = '__all__'

class BestOfImportedJewellery(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfImportedJewellerySerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfImportedJewellery
        fields = '__all__'

class BestOfFingerRings(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfFingerRingsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfFingerRings
        fields = '__all__'

class BestOfEarRings(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfEarRingsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfEarRings
        fields = '__all__'


class BestOfChains(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfChainsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfChains
        fields = '__all__'

class BestOfBracelets(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)


class BestOfBraceletsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfBracelets
        fields = '__all__'

class BestOfBangles(models.Model):
    pojos = models.ForeignKey(POJOS, on_delete=models.CASCADE)

class BestOfBanglesSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestOfBangles
        fields = '__all__'


class FeatureProductsSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = FeatureProducts
        fields = '__all__'

class BestSellersSerializer(serializers.ModelSerializer):
    pocos = PojoListSerializer()

    class Meta:
        model = BestSellers
        fields = '__all__'

	
	