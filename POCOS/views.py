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


from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import POCOS
from .serializers import PocoListSerializer

@api_view(['GET'])
def product_search(request):
    print("🚀 THIS FUNCTION IS RUNNING!")
    query = request.GET.get('q', '').strip()
    print(f"🔍 Received Query: {query}")

    return Response({"query_received": query})
