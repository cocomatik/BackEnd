from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q, F
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity
from .models import POCOS, Review, Category
from .serializers import PocoListSerializer, PocoDetailSerializer, ReviewSerializer, CategorySerializer
from Accounts.decorators import token_auth_required

@api_view(['GET'])
def get_all_pocos(request):
    pocos = POCOS.objects.all()
    serializer = PocoListSerializer(pocos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    
    if not categories.exists():
        return Response({"detail": "No categories found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_poco_details(request, sku):
    poco = get_object_or_404(POCOS, sku=sku)  # Use SKU instead of poco_id
    serializer = PocoDetailSerializer(poco)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@token_auth_required  # Secure review posting
def reviews(request, sku):
    poco = get_object_or_404(POCOS, sku=sku)  # Use SKU instead of poco_id

    if request.method == 'GET':
        reviews = poco.reviews.all()
        
        if not reviews.exists():
            return Response({"detail": "No reviews found for this product."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(poco=poco, user=request.user)  # Ensure the review is linked to the user
            return Response({"message": "Review added successfully!", "review": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

    full_text_results = POCOS.objects.annotate(
        search=SearchVector('title', 'description')
    ).filter(Q(search=SearchQuery(query)))

    partial_results = POCOS.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(sku__icontains=query)  # Include SKU in search
    )

    fuzzy_results = POCOS.objects.annotate(
        similarity=TrigramSimilarity('title', query)
    ).filter(similarity__gt=0.3)

    products = (full_text_results | partial_results | fuzzy_results).distinct()

    if not products.exists():
        return Response({"detail": "No products match the given query."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PocoListSerializer(products, many=True)
    return Response(serializer.data)
