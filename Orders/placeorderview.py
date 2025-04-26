# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

# from Delivery.shiprocket import ShiprocketAPI
# from Accounts.decorators import token_auth_required
# from Accounts.models import Address
# from .models import Cart, CartItem, Order




    #     shiprocket = ShiprocketAPI()
    #     shiprocket_response = shiprocket.create_order(order=order)

    #     logger.info(f"Shiprocket Response for Order {order.order_number}: {shiprocket_response}")

    #     if "error" in shiprocket_response:
    #         ordered_cart.status = "FAIL"
    #         ordered_cart.remark = str(shiprocket_response.get("message", "Shiprocket error"))
    #         ordered_cart.save()
    #         return Response({
    #             "message": "Order created, but failed to integrate with Shiprocket.",
    #             "order_id": order.order_number,
    #             "shiprocket_error": shiprocket_response
    #         }, status=status.HTTP_206_PARTIAL_CONTENT)

    #     # Success flow
        

        

    #     ordered_cart.status = "SUCCESS"
    #     ordered_cart.shiprocket_order_id = shiprocket_response.get("order_id", "")
    #     ordered_cart.remark = "Shiprocket order placed successfully"
    #     ordered_cart.save()

    #     # New cart for the user
    #     Cart.objects.create(user=user, status="pending")
