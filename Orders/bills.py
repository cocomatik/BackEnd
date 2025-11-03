from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from xhtml2pdf import pisa
from .models import Order
import io

@api_view(['GET'])
def generate_invoice(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


    # Prepare context for the HTML template
    context = {
        'order': order,
        'order_items': order.cart.cart_items.all(),
        'user': order.user,
        'address': order.address,
    }

    # Render HTML template with context data
    html_content = render_to_string('Orders/Bills/invoice_template.html', context)

    return HttpResponse(html_content)
