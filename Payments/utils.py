import json, base64, hashlib, hmac, requests

MERCHANT_ID = 'your_merchant_id'
SALT_KEY = 'your_salt_key'
SALT_INDEX = 'your_salt_index'
BASE_URL = 'https://api-preprod.phonepe.com/apis/pg-sandbox'
REDIRECT_URL = 'https://yourdomain.com/api/payment/callback/'

def initiate_phonepe_payment(order):
    payload = {
        "merchantId": MERCHANT_ID,
        "transactionId": str(order.order_number),
        "amount": int(order.total_price * 100),  
        "merchantUserId": str(order.user.id),
        "redirectUrl": REDIRECT_URL,
        "redirectMode": "POST",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }

    base64_payload = base64.b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(SALT_KEY.encode(), base64_payload.encode(), hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": f"{signature}###{SALT_INDEX}"
    }

    response = requests.post(
        f"{BASE_URL}/pg/v1/pay",
        headers=headers,
        json={"request": base64_payload}
    )

    if response.status_code == 200 and response.json().get("success"):
        redirect_url = response.json()["data"]["instrumentResponse"]["redirectInfo"]["url"]
        return {"redirect_url": redirect_url}
    else:
        raise Exception("PhonePe payment initiation failed.")
