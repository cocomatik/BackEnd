import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from POCOS.modelsxs import BestSellers as BSC,BestSellersSerializer as BSCS 
from POJOS.modelsxs import BestSellers as BSJ,BestSellersSerializer as BSJS
from rest_framework.response import Response

from POCOS.models import POCOS
from POJOS.models import POJOS

@api_view(['GET'])
def home_best_sellers(request):
    bsc_products = BSC.objects.filter(id=1)
    bsj_products = BSJ.objects.filter(id=1)

    bsc_serialized = BSCS(bsc_products, many=True).data
    bsj_serialized = BSJS(bsj_products, many=True).data

    combined_data = bsc_serialized + bsj_serialized
    random.shuffle(combined_data)

    return Response(combined_data)


from rest_framework import status
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from POCOS.serializers import PocoListSerializer
from POJOS.serializers import PojoListSerializer

from POCOS.models import POCOS
from POJOS.models import POJOS


@api_view(['GET'])
def all_products_list(request):
    pocos = POCOS.objects.all().values('title', 'sku', 'description')
    pojos = POJOS.objects.all().values('title', 'sku', 'description')

    results = []

    for p in pocos:
        results.append({
            "type": "poco",
            "title": p['title'],
            "sku": p['sku'],
            "description":p['description']
        })
    for p in pojos:
        results.append({
            "type": "pojo",
            "title": p['title'],
            "sku": p['sku'],
            "description":p['description']
        })
    return Response(results)


from django.contrib.postgres.search import SearchVector
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def combined_search(request):
    query = request.GET.get('q', '')

    pocos = POCOS.objects.all()
    pojos = POJOS.objects.all()

    if query:
        pocos = pocos.annotate(search=SearchVector('title', 'description', 'brand')).filter(search=query)
        pojos = pojos.annotate(search=SearchVector('title', 'description', 'brand')).filter(search=query)

    # Serialize separately with type annotation
    pocos_data = PocoListSerializer(pocos, many=True).data
    pojos_data = PojoListSerializer(pojos, many=True).data

    # Combine and sort by created_at (if needed)
    combined = sorted(pocos_data + pojos_data, key=lambda x: x['created_at'], reverse=True)

    # Paginate manually
    paginator = PageNumberPagination()
    paginator.page_size = 100
    paginated = paginator.paginate_queryset(combined, request)

    return paginator.get_paginated_response(paginated)
