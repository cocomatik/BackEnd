from django.db import models
from cloudinary.models import CloudinaryField

class CosmeticAdds(models.Model):
    img=CloudinaryField('image', folder='pocos/Adds/')

class jwelleryAdds(models.Model):
    img=CloudinaryField('image', folder='pojos/Adds/')


from rest_framework import serializers

class CosmeticAddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CosmeticAdds
        fields = ['img']

class JwelleryAddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = jwelleryAdds
        fields = ['img']
