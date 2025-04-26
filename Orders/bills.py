from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Order

def generate_invoice(request, order_id):
    # Fetch order data from the database
    order = Order.objects.get(id=order_id)    
    # Prepare the context for the template
    context = {
        'order': order,
        'order_items': order.cart.cart_items.all(),
        'user': order.user,
        'address': order.address,
    }
    
    # Render HTML from template
    html_content = render_to_string('Orders\Bills\invoice_template.html', context)
    
    # Generate PDF from HTML
    pdf = HTML(string=html_content).write_pdf()
    
    # Return PDF as response without saving to file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'
    
    return response
