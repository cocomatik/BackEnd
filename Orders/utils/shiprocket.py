import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ShiprocketAPI:
    BASE_URL = "https://apiv2.shiprocket.in/v1/external"

    def __init__(self):
        self.token = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticates and retrieves the access token for Shiprocket API.
        """
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "email": settings.SHIPROCKET_EMAIL,
            "password": settings.SHIPROCKET_PASSWORD
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()  # Raises an error for HTTP 4xx/5xx
            data = response.json()
            self.token = data.get("token")

            if not self.token:
                logger.error("Shiprocket authentication failed: No token received.")
                raise ValueError("Authentication failed: No token received from Shiprocket.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Shiprocket authentication error: {e}")
            self.token = None

    def refresh_token_if_needed(self):
        """Refresh the token if it's missing or expired"""
        if not self.token:
            self.authenticate()

    def create_order(self, order):
        """
        Creates an order in Shiprocket for shipping.
        """
        self.refresh_token_if_needed()

        url = f"{self.BASE_URL}/orders/create/adhoc"

        # Ensure order.cart has items
        cart_items = order.cart.cart_items.all()
        if not cart_items.exists():
            logger.warning(f"Order {order.id} has no items. Skipping Shiprocket request.")
            return {"error": "No items in the cart for shipping."}

        items = [
            {
                "name": item.product.title,
                "sku": str(item.product.id),  
                "units": item.quantity,
                "selling_price": float(item.product.price)
            }
            for item in cart_items
        ]

        # Calculate total value
        total_value = sum(item.quantity * item.product.price for item in cart_items)

        payload = {
            "order_id": str(order.id),
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "pickup_location": "Primary Warehouse",

            # ✅ Billing Address
            "billing_customer_name": order.address.name,
            "billing_address": order.address.street,
            "billing_city": order.address.city,
            "billing_pincode": order.address.pincode,
            "billing_state": order.address.state,
            "billing_country": "India",
            "billing_email": order.user.email,
            "billing_phone": str(order.user.phone),

            # ✅ Shipping Address
            "shipping_is_billing": True,
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
            "sub_total": float(total_value),
            "length": 10, "breadth": 10, "height": 10, "weight": 1.0
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            response_data = response.json()

            # Log successful response
            logger.info(f"Shiprocket Order {order.id} Response: {response_data}")
            return response_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Shiprocket order creation failed for Order {order.id}: {e}")
            return {"error": f"Shiprocket request failed: {str(e)}"}
