from django.urls import path,include
import POCOS.urls as PU
urlpatterns = [
    path('pocos', include(PU)),
]