from django.db import models
from .models import POJOS

from rest_framework import serializers
from .serializers import PojoListSerializer

from django.db import models
from .models import POJOS

class FeatureProducts(models.Model):
    pojos = models.ManyToManyField(POJOS)  # No restriction

class BestSellers(models.Model):
    pojos = models.ManyToManyField(POJOS)  # No restriction

class BestOfWeddingJewellery(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Wedding Jewellery'})

class BestOfPendants(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Pendants'})

class BestOfNoseRings(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Nose Rings'})

class BestOfNecklace(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Necklace'})

class BestOfOneGramGoldenJewellery(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'One Gram Golden Jewellery'})

class BestOfImportedJewellery(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Imported Jewellery'})

class BestOfFingerRings(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Finger Rings'})

class BestOfEarRings(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Ear Rings'})

class BestOfChains(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Chains'})

class BestOfBracelets(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Bracelets'})

class BestOfBangles(models.Model):
    pojos = models.ManyToManyField(POJOS, limit_choices_to={'category': 'Bangles'})

class BestOfWeddingJewellerySerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfWeddingJewellery
        fields = '__all__'

class BestOfPendantsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfPendants
        fields = '__all__'

class BestOfNoseRingsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfNoseRings
        fields = '__all__'


class BestOfNecklaceSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfNecklace
        fields = '__all__'

class BestOfOneGramGoldenJewellerySerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfOneGramGoldenJewellery
        fields = '__all__'

class BestOfImportedJewellerySerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfImportedJewellery
        fields = '__all__'

class BestOfFingerRingsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfFingerRings
        fields = '__all__'

class BestOfEarRingsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfEarRings
        fields = '__all__'


class BestOfChainsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfChains
        fields = '__all__'



class BestOfBraceletsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfBracelets
        fields = '__all__'


class BestOfBanglesSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestOfBangles
        fields = '__all__'


class FeatureProductsSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = FeatureProducts
        fields = '__all__'

class BestSellersSerializer(serializers.ModelSerializer):
    pojos = PojoListSerializer(many=True)

    class Meta:
        model = BestSellers
        fields = '__all__'

	
	