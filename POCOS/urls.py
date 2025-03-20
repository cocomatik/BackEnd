from django.urls import path,include
from .views import get_all_pocos, get_poco_details, reviews,search_products,get_categories


from rest_framework.routers import DefaultRouter
from .xsviews import (
    FeatureProductsViewSet,BestOfSkinCareViewSet,
    BestOfImportedProductsViewSet, BestOfHairCareViewSet, BestOfFragranceViewSet,
    BestOfColorCosmeticViewSet, BestOfBodyCareViewSet
)

router = DefaultRouter()
router.register(r'feature-products', FeatureProductsViewSet, basename='feature-products')
# router.register(r'best-sellers', BestSellersViewSet, basename='best-sellers')
router.register(r'best-of-skincare', BestOfSkinCareViewSet, basename='best-of-skincare')
router.register(r'best-of-imported-products', BestOfImportedProductsViewSet, basename='best-of-imported-products')
router.register(r'best-of-haircare', BestOfHairCareViewSet, basename='best-of-haircare')
router.register(r'best-of-fragrance', BestOfFragranceViewSet, basename='best-of-fragrance')
router.register(r'best-of-color-cosmetic', BestOfColorCosmeticViewSet, basename='best-of-color-cosmetic')
router.register(r'best-of-bodycare', BestOfBodyCareViewSet, basename='best-of-bodycare')



urlpatterns = [
    path('', get_all_pocos, name='all-pocos'),
    path('categories/', get_categories, name='pocos-categories'),
    path('details/<str:poco_id>/', get_poco_details, name='poco-details'),
    path('reviews/<str:poco_id>/', reviews, name='add-review'),
    path('search/', search_products, name='product-search'),
    path('search/', search_products, name='product-search'),
    path('xs/', include(router.urls)),
]


