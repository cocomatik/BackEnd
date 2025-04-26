from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import Response
from Orders.models import Order
from Delivery.shiprocket import ShiprocketAPI
from Delivery.models import ShiprocketOrder
from rest_framework import status

def create_shipment(request):
    order_number=request.POST.get('order_number')
    length=request.POST.get('length')
    breadth=request.POST.get('breadth')
    height=request.POST.get('height')
    weight=request.POST.get('weight')
    comment=request.POST.get('comment')
    reseller_name=request.POST.get('reseller_name')
    company_name=request.POST.get('company_name')

    order=get_object_or_404(Order,order_number=order_number)


    try:
        ship=ShiprocketAPI()
        ship_response=ship.create_order(order,length,breadth,height,weight,comment,reseller_name,company_name)

        ShiprocketOrder.objects.create(
            order=order,
            shiprocket_order_id=ship_response.get('order_id'),
            shipment_id=ship_response.get('shipment_id'),
            status=ship_response.get('status'),
            status_code=ship_response.get('status_code'),
            awb_code=ship_response.get('awb_code'),
            courier_name=ship_response.get('courier_name'),
        )

        return redirect("order_list")

    except Exception as e:
        return Response({
            "error": "Something went wrong during order placement.",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
