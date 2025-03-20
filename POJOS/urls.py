from django.urls import path
from .views import get_all_pojos, get_pojo_details, reviews,search_products,get_categories

urlpatterns = [
    path('', get_all_pojos, name='all-pojos'),
    path('categories/', get_categories, name='pojos-categories'),
    path('details/<str:pojo_id>/', get_pojo_details, name='pojo-details'),
    path('reviews/<str:pojo_id>/', reviews, name='add-review'),
    path('search/', search_products, name='product-search'),
]
