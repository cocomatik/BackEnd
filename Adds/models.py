from django.db import models


class CosmeticAdds(models.Model):
    img=models.ImageField(upload_to='pocos/Adds/')

class jwelleryAdds(models.Model):
    img=models.ImageField(upload_to='pojos/Adds/')


from rest_framework import serializers

class CosmeticAddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CosmeticAdds
        fields = ['img']

class JwelleryAddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = jwelleryAdds
        fields = ['img']
