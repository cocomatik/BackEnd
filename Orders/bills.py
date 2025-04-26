from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from xhtml2pdf import pisa
from .models import Order

@api_view(['GET'])
def generate_invoice(request, order_number):
    try:
        # Fetch order data from the database
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Prepare the context for the template
    context = {
        'order': order,
        'order_items': order.cart.cart_items.all(),
        'user': order.user,
        'address': order.address,
    }

    # Render HTML from template
    html_content = render_to_string('Orders/Bills/invoice_template.html', context)

    # Create an HTTP response object with the content type for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'

    # Use xhtml2pdf to convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    if pisa_status.err:
        return Response({"error": "Error generating PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
