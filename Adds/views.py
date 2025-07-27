# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CosmeticAdds, jwelleryAdds, CosmeticAddsSerializer, JwelleryAddsSerializer

@api_view(['GET'])
def Cadds(request):
    adds = CosmeticAdds.objects.all()
    serializer = CosmeticAddsSerializer(adds, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Jadds(request):
    adds = jwelleryAdds.objects.all()
    serializer = JwelleryAddsSerializer(adds, many=True)
    return Response(serializer.data)
