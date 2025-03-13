from django.urls import path
from .views import get_all_pocos, get_poco_details, add_review

urlpatterns = [
    path('pocos/', get_all_pocos, name='all-pocos'),
    path('pocos/<str:poco_id>/', get_poco_details, name='poco-details'),
    path('pocos/<str:poco_id>/review/', add_review, name='add-review'),
]
