from rest_framework import viewsets
from .modelsxs import (
    FeatureProducts, BestSellers, BestOfWeddingJewellery, BestOfPendants,
    BestOfNoseRings, BestOfNecklace, BestOfOneGramGoldenJewellery, BestOfImportedJewellery,
    BestOfFingerRings, BestOfEarRings, BestOfChains, BestOfBracelets, BestOfBangles,BestOfImportedJewellerySerializer,
    FeatureProductsSerializer, BestSellersSerializer, BestOfWeddingJewellerySerializer, BestOfPendantsSerializer,
    BestOfNoseRingsSerializer, BestOfNecklaceSerializer, BestOfOneGramGoldenJewellerySerializer,
    BestOfFingerRingsSerializer, BestOfEarRingsSerializer, BestOfChainsSerializer, BestOfBraceletsSerializer, BestOfBanglesSerializer
)

class FeatureProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureProducts.objects.all()
    serializer_class = FeatureProductsSerializer

# class BestSellersViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = BestSellers.objects.all()
#     serializer_class = BestSellersSerializer

class BestOfWeddingJewelleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfWeddingJewellery.objects.all()
    serializer_class = BestOfWeddingJewellerySerializer

class BestOfPendantsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfPendants.objects.all()
    serializer_class = BestOfPendantsSerializer


class BestOfNoseRingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfNoseRings.objects.all()
    serializer_class = BestOfNoseRingsSerializer

class BestOfNecklaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfNecklace.objects.all()
    serializer_class = BestOfNecklaceSerializer

class BestOfOneGramGoldenJewelleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfOneGramGoldenJewellery.objects.all()
    serializer_class = BestOfOneGramGoldenJewellerySerializer

class BestOfImportedJewelleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfImportedJewellery.objects.all()
    serializer_class = BestOfImportedJewellerySerializer

class BestOfFingerRingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfFingerRings.objects.all()
    serializer_class = BestOfFingerRingsSerializer

class BestOfEarRingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfEarRings.objects.all()
    serializer_class = BestOfEarRingsSerializer

class BestOfChainsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfChains.objects.all()
    serializer_class = BestOfChainsSerializer

class BestOfBraceletsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfBracelets.objects.all()
    serializer_class = BestOfBraceletsSerializer

class BestOfBanglesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BestOfBangles.objects.all()
    serializer_class = BestOfBanglesSerializer