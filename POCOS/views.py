from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import POCOS, Review
from .serializers import PocoListSerializer, PocoDetailSerializer, ReviewSerializer

from Accounts.decorators import token_auth_required,session_auth_required

@api_view(['GET'])
def get_all_pocos(request):
    pocos = POCOS.objects.all()
    serializer = PocoListSerializer(pocos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_poco_details(request, poco_id):
    poco = get_object_or_404(POCOS, poco_id=poco_id)
    serializer = PocoDetailSerializer(poco)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def reviews(request, poco_id):
    poco = get_object_or_404(POCOS, poco_id=poco_id)

    if request.method == 'GET':
        reviews = poco.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(poco=poco)
            return Response({"message": "Review added successfully!", "review": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Q, F
from django.contrib.postgres.search import SearchVector, SearchQuery,TrigramSimilarity
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import POCOS
from .serializers import PocoListSerializer

@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', ' ').strip()
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

    full_text_results = POCOS.objects.annotate(
        search=SearchVector('title', 'description')
    ).filter(Q(search=SearchQuery(query)))

    partial_results = POCOS.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    fuzzy_results = POCOS.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.3)

    products = (full_text_results | partial_results).distinct()

    if not products.exists():
        return Response({"detail": "No products match the given query."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PocoListSerializer(products, many=True)
    return Response(serializer.data)