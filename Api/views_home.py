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
