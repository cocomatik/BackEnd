import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from POCOS.modelsxs import BestSellers as BSC,BestSellersSerializer as BSCS 
from POJOS.modelsxs import BestSellers as BSJ,BestSellersSerializer as BSJS
from rest_framework.response import Response

@api_view(['GET'])
def home_best_sellers(request):
    bsc_products = BSC.objects.filter(id=1)
    bsj_products = BSJ.objects.filter(id=1)

    bsc_serialized = BSCS(bsc_products, many=True).data
    bsj_serialized = BSJS(bsj_products, many=True).data

    combined_data = bsc_serialized + bsj_serialized
    random.shuffle(combined_data)

    return Response(combined_data)
