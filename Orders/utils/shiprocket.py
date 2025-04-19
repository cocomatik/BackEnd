# shiprocket.py
import logging
import requests
logger=logging.root
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
            # "email": "sanskaricoders@gmail.com",
            "password": "&%2bZrJC4mWA9vH"  # Consider moving these credentials to environment variables for security
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
            logger.info("Token is missing or expired. Refreshing...")
            self.authenticate()

    def create_order(self, order):
        """
        Create Shiprocket order using real order data.
        """
        ordered_items = order.cart.cart_items.all()

        items_payload = []

        for item in ordered_items:
            product_model = item.product_type.model_class() if item.product_type else None
            product = product_model.objects.filter(sku=item.sku).first() if product_model else None

            items_payload.append({
                "name": str(item.title),  # or item.sku if no title field
                "sku": item.sku,
                "units": item.quantity,
                "selling_price": float(product.price) if product else 0
            })


        shipping_address = order.address

        payload = {
            "order_id": str(order.order_number),
            "order_date": str(order.created_at.date()),
            "pickup_location": "Primary",  # Replace with your Shiprocket location name
            "billing_customer_name": shipping_address.name,
            "billing_address": f"{shipping_address.house_no},{shipping_address.street}",
            "billing_city": shipping_address.city,
            "billing_pincode": shipping_address.pincode,
            "billing_state": shipping_address.state,
            "billing_country": "India",
            "billing_email": order.user.email,
            "billing_phone": shipping_address.contact_no,
            "order_items": items_payload,
            "payment_method": "Prepaid" if order.payment_mode == "PG" else "COD",
            "sub_total": float(order.cart.value)
        }

        # Call Shiprocket API here (pseudo-code)
        response = self.make_api_request(payload)
        return response

    def make_api_request(self, payload):
        # actual request logic here using `requests.post()` etc.
        return {"dummy": "success"}
