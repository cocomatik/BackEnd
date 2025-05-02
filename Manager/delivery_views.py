from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from Orders.models import Order, OrderHistory, OrderHistoryItem
from Delivery.shiprocket import ShiprocketAPI
from Delivery.models import ShiprocketOrder
from django.contrib import messages
from django.db import transaction

def create_shipment(request):
    # Retrieve necessary data from POST
    order_number = request.POST.get('order_number')
    length = request.POST.get('length')
    breadth = request.POST.get('breadth')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    comment = request.POST.get('comment')
    reseller_name = request.POST.get('reseller_name')
    company_name = request.POST.get('company_name')


    # Ensure the order exists
    order = get_object_or_404(Order, order_number=order_number)

    # Check if all required fields are present
    if not all([order_number, length, breadth, height, weight]):
        messages.error(request, "All shipment details are required.")
        return redirect("order_list")

    try:
        with transaction.atomic():
            order_his = OrderHistory.objects.create(
                order=order,
                user=order.user,
                address=order.address,
                order_number=order.order_number,
                payment_mode=order.payment_mode,
                sub_total=order.sub_total,
                total_price=order.total_price,
                discount=order.discount,
                tax=order.tax,
                shipping_charges=order.shipping_charges,
                packaging_charges=order.packaging_charges,
                cod_charges=order.cod_charges,
                handling_charges=order.handling_charges,
                length=length,
                breadth=breadth,
                height=height,
                weight=weight,
                comment=comment,
                reseller_name=reseller_name,
                company_name=company_name,
            )
            order_his.save()
        
            # Create OrderHistoryItems
            for item in order.cart.cart_items.all():
                OrderHistoryItem.objects.create(
                    order_history=order_his,
                    title=item.title,
                    sku=item.sku,
                    quantity=item.quantity,
                    selling_price=item.product.price,
                    discount=item.product.discount,
                    product_type=item.product_type,
                    product=item.product,
                )

            ship = ShiprocketAPI()
            ship_response = ship.create_order(
                order, length, breadth, height, weight, comment, reseller_name, company_name
            )

            
            # Store Shiprocket order info in your database
            ShiprocketOrder.objects.create(
                orderH=order_his,
                shiprocket_order_id=ship_response.get('order_id'),
                shipment_id=ship_response.get('shipment_id'),
                status=ship_response.get('status'),
                status_code=ship_response.get('status_code'),
                awb_code=ship_response.get('awb_code'),
                courier_name=ship_response.get('courier_name'),
            )
            
            order_his.shiprocket_order_id=ship_response.get('order_id')
            order_his.save()

            order.status = "SHIPMENT_CREATED"
            order.save()

            

            # Redirect the user after success
            messages.success(request, "Shipment created successfully!")
            return redirect("shipment_details")

    except Exception as e:
        print(e)
        # Log the error and show a friendly message
        messages.error(request, f"Error creating shipment: {str(e)}")
        return redirect("shipment_details")


def pending_shipments(request):
    order_list = Order.objects.filter(status="ORDERED").order_by('-created_at')

    return render(request, "Manager\shipment\pendingShipment.html", {"order_list": order_list})


def pending_SDetails(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'Manager\shipment\pendingSDetails.html', {'order': order})