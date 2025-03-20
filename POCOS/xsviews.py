from rest_framework import viewsets
from .modelsxs import (
    FeatureProducts, BestSellers, BestOfSkinCare,
    BestOfImportedProducts, BestOfHairCare, BestOfFragrance,
    BestOfColorCosmetic, BestOfBodyCare,FeatureProductsSerializer, BestSellersSerializer, BestOfSkinCareSerializer,
    BestOfImportedProductsSerializer, BestOfHairCareSerializer, BestOfFragranceSerializer,
    BestOfColorCosmeticSerializer, BestOfBodyCareSerializer
)

class FeatureProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureProducts.objects.all()
    serializer_class = FeatureProductsSerializer

class BestSellersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestSellers.objects.all()
    serializer_class = BestSellersSerializer

class BestOfSkinCareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfSkinCare.objects.all()
    serializer_class = BestOfSkinCareSerializer

class BestOfImportedProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfImportedProducts.objects.all()
    serializer_class = BestOfImportedProductsSerializer

class BestOfHairCareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfHairCare.objects.all()
    serializer_class = BestOfHairCareSerializer

class BestOfFragranceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfFragrance.objects.all()
    serializer_class = BestOfFragranceSerializer

class BestOfColorCosmeticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfColorCosmetic.objects.all()
    serializer_class = BestOfColorCosmeticSerializer

class BestOfBodyCareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfBodyCare.objects.all()
    serializer_class = BestOfBodyCareSerializer
