import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ShiprocketAPI:
    BASE_URL = "https://apiv2.shiprocket.in/v1/external"
    
    def __init__(self):
        self.token = self.authenticate()

    def authenticate(self):
        """Authenticate and return the token."""
        try:
            response = requests.post(
                f"{self.BASE_URL}/auth/login",
                json={
                    "email": settings.SHIPROCKET_EMAIL,
                    "password": settings.SHIPROCKET_PASSWORD,
                }
            )
            response.raise_for_status()
            return response.json().get("token")
        except Exception as e:
            logger.error(f"[Shiprocket Auth Error] {str(e)}")
            return None

    def create_order(self,order,length,breadth,height,weight,comment,reseller_name,company_name):
        if not self.token:
            return {"error": "Authentication failed. No token received."}

        address = order.address
        cart_items = order.cart.cart_items.all()

        # Construct line items
        line_items = []
        for item in cart_items:
            line_items.append({
                "name": item.product.title,
                "sku": item.sku,
                "units": item.quantity,
                "selling_price": float(item.product.price),
                "discount": 0,
                "tax": 0,
            })
        

        payload = {
            "order_id": str(order.order_number),
            "order_date": str(order.created_at.date()),
            "pickup_location": "Home",
            # "channel_id": "",  # optional
            "comment": str(comment),
            "reseller_name":str(reseller_name),
            "company_name" :str(company_name),
            "billing_customer_name": address.name,
            "billing_last_name": getattr(address, "last_name", ""),
            "billing_address": address.street,
            # "billing_address_2": "",
            "billing_city": address.city,
            "billing_pincode": address.pincode,
            "billing_state": address.state,
            "billing_country": "India",
            "billing_email": address.user.email,
            "billing_phone": address.contact_no,
            "shipping_is_billing": True,
            "order_items": line_items,
            "payment_method": "COD" if order.payment_mode == "COD" else "Prepaid",
            "sub_total": float(order.sub_total),
            "length": str(length),
            "breadth":str(breadth),
            "height": str(height),
            "weight": str(weight),
            }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/orders/create/adhoc",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"[Shiprocket Error] HTTP Error: {http_err} | Response: {response.text}")
            return {
                "error": "http_error",
                "message": str(http_err),
                "details": response.text
            }
        except Exception as e:
            logger.error(f"[Shiprocket Error] Unexpected Error: {str(e)}")
            return {"error": "unexpected", "message": str(e)}
    

    def get_order_details(self, shiprocket_order_id):
        url = f"https://apiv2.shiprocket.in/v1/external/orders/show/{shiprocket_order_id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        return response.json()
