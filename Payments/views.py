from rest_framework.decorators import api_view
from rest_framework.response import Response
from Orders.models import Order  
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt
@api_view(["POST"])
def phonepe_callback(request):
    transaction_id = request.data.get("transactionId")

    try:
        order = Order.objects.get(order_number=transaction_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    # Optionally verify again via PhonePe status check API (recommended)
    order.status = "ORDERED"
    order.ordered_at = timezone.now()
    order.save()

    return Response({"message": "Payment successful. Order confirmed."}, status=200)
