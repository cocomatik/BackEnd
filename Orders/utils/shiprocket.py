import requests
from django.conf import settings

class ShiprocketAPI:
    BASE_URL = "https://apiv2.shiprocket.in/v1/external"
    
    def __init__(self):
        self.token = self.authenticate()

    def authenticate(self):
        """
        Authenticates and retrieves the access token for Shiprocket API.
        """
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "email": settings.SHIPROCKET_EMAIL,
            "password": settings.SHIPROCKET_PASSWORD
        }
        response = requests.post(url, json=payload)
        data = response.json()
        return data.get("token")
    
    def create_order(self, order):
        """
        Creates an order in Shiprocket for shipping.
        """
        url = f"{self.BASE_URL}/orders/create/adhoc"

        items = [
            {
                "name": item.product.title,
                "sku": str(item.product.id),  
                "units": item.quantity,
                "selling_price": float(item.product.price)
            }
            for item in order.cart.cart_items.all()
        ]

        payload = {
            "order_id": str(order.id),
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "pickup_location": "Primary Warehouse",

            # ✅ Billing Address (Required)
            "billing_customer_name": order.address.name,
            "billing_address": order.address.street,
            "billing_city": order.address.city,
            "billing_pincode": order.address.pincode,
            "billing_state": order.address.state,
            "billing_country": "India",
            "billing_email": order.user.email,
            "billing_phone": str(order.user.phone),

            # ✅ Shipping Address (Required)
            "shipping_is_billing": True,  # If false, add shipping fields below
            "shipping_customer_name": order.user.name,
            "shipping_address": order.address.street,
            "shipping_city": order.address.city,
            "shipping_pincode": order.address.pincode,
            "shipping_state": order.address.state,
            "shipping_country": "India",
            "shipping_email": order.user.email,
            "shipping_phone": str(order.user.phone),

            "order_items": items,
            "payment_method": "COD" if order.payment_mode == "cashondelivery" else "Prepaid",
            "sub_total": float(order.cart.value),
            "length": 10, "breadth": 10, "height": 10, "weight": 1.0
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
