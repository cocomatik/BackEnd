from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import POJOS, Review
from .serializers import PojoImageSerializer, PojoDetailSerializer,PojoListSerializer, ReviewSerializer

from Accounts.decorators import token_auth_required,session_auth_required

@api_view(['GET'])
def get_all_pojos(request):
    pojos = POJOS.objects.all()
    serializer = PojoListSerializer(pojos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_pojo_details(request, pojo_id):
    pojo = get_object_or_404(POJOS, pojo_id=pojo_id)
    serializer = PojoDetailSerializer(pojo)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def reviews(request, pojo_id):
    pojo = get_object_or_404(POJOS, pojo_id=pojo_id)

    if request.method == 'GET':
        reviews = pojo.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(pojo=pojo)
            return Response({"message": "Review added successfully!", "review": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Q, F
from django.contrib.postgres.search import SearchVector, SearchQuery,TrigramSimilarity

@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', ' ').strip()
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

    full_text_results = POJOS.objects.annotate(
        search=SearchVector('title', 'description')
    ).filter(Q(search=SearchQuery(query)))

    partial_results = POJOS.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    fuzzy_results = POJOS.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.3)

    products = (full_text_results | partial_results).distinct()

    if not products.exists():
        return Response({"detail": "No products match the given query."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PojoListSerializer(products, many=True)
    return Response(serializer.data)