from django.urls import path
from .views import get_all_pocos, get_poco_details, reviews,search_products,get_categories

urlpatterns = [
    path('', get_all_pocos, name='all-pocos'),
    path('categories/', get_categories, name='pocos-categories'),
    path('details/<str:poco_id>/', get_poco_details, name='poco-details'),
    path('reviews/<str:poco_id>/', reviews, name='add-review'),
    path('search/', search_products, name='product-search'),
]
