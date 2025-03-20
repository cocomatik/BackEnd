from django.urls import path,include
from .views import get_all_pojos, get_pojo_details, reviews,search_products,get_categories
from rest_framework.routers import DefaultRouter

from .xsviews import FeatureProductsViewSet,BestSellersViewSet,BestOfWeddingJewelleryViewSet,BestOfBanglesViewSet,BestOfBraceletsViewSet,BestOfChainsViewSet,BestOfEarRingsViewSet,BestOfFingerRingsViewSet,BestOfNecklaceViewSet,BestOfPendantsViewSet,BestOfNoseRingsViewSet,BestOfImportedJewelleryViewSet,BestOfOneGramGoldenJewelleryViewSet


router = DefaultRouter()
router.register(r'feature-products', FeatureProductsViewSet, basename='feature-products')
router.register(r'best-sellers', BestSellersViewSet, basename='best-sellers')
router.register(r'best-of-wedding-jewellery', BestOfWeddingJewelleryViewSet, basename='best-of-wedding-jewellery')
router.register(r'best-of-pendants', BestOfPendantsViewSet, basename='best-of-pendants')
router.register(r'best-of-nose-rings', BestOfNoseRingsViewSet, basename='best-of-nose-rings')
router.register(r'best-of-necklace', BestOfNecklaceViewSet, basename='best-of-necklace')
router.register(r'best-of-one-gram-golden-jewellery', BestOfOneGramGoldenJewelleryViewSet, basename='best-of-one-gram-golden-jewellery')
router.register(r'best-of-imported-jewellery', BestOfImportedJewelleryViewSet, basename='best-of-imported-jewellery')
router.register(r'best-of-finger-rings', BestOfFingerRingsViewSet, basename='best-of-finger-rings')
router.register(r'best-of-ear-rings', BestOfEarRingsViewSet, basename='best-of-ear-rings')
router.register(r'best-of-chains', BestOfChainsViewSet, basename='best-of-chains')
router.register(r'best-of-bracelets', BestOfBraceletsViewSet, basename='best-of-bracelets')
router.register(r'best-of-bangles', BestOfBanglesViewSet, basename='best-of-bangles')


urlpatterns = [
    path('', get_all_pojos, name='all-pojos'),
    path('categories/', get_categories, name='pojos-categories'),
    path('details/<str:pojo_id>/', get_pojo_details, name='pojo-details'),
    path('reviews/<str:pojo_id>/', reviews, name='add-review'),
    path('search/', search_products, name='product-search'),
    path('xs/',include(router.urls)),
]
