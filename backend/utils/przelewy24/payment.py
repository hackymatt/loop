from rest_framework import status
import requests
from typing import List
from purchase.models import Purchase, Payment
from profile.models import Profile
from config_global import (
    FRONTEND_URL,
    PAYMENT_SERVER,
    PAYMENT_API_KEY,
    PAYMENT_CRC,
    PAYMENT_MERCHANT_ID,
    PAYMENT_STORE_ID,
)
import json
import base64
import hashlib


class Przelewy24Api:
    def __init__(self) -> None:
        self.register_url = f"{PAYMENT_SERVER}/api/v1/transaction/register"
        self.verify_url = f"{PAYMENT_SERVER}/api/v1/transaction/verify"

        credentials = f"{PAYMENT_STORE_ID}:{PAYMENT_API_KEY}".encode("utf-8")
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(credentials).decode('utf-8')}",
            "Content-Type": "application/json",
        }

    def _create_sign(self, data):
        json_data = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha384(json_data.encode("utf-8")).hexdigest()

    def _create_register_sign(self, payment: Payment):
        data = {
            "sessionId": str(payment.session_id),
            "merchantId": int(PAYMENT_MERCHANT_ID),
            "amount": int(payment.amount),
            "currency": "PLN",
            "crc": PAYMENT_CRC,
        }
        return self._create_sign(data=data)

    def _create_verify_sign(self, payment: Payment):
        data = {
            "sessionId": str(payment.session_id),
            "orderId": payment.order_id,
            "amount": payment.amount,
            "currency": "PLN",
            "crc": PAYMENT_CRC,
        }
        return self._create_sign(data=data)

    def register(self, client: Profile, payment: Payment, purchases: List[Purchase]):
        raise ValueError("hererere")
        data = {
            "merchantId": PAYMENT_MERCHANT_ID,
            "posId": PAYMENT_STORE_ID,
            "sessionId": str(payment.session_id),
            "amount": payment.amount,
            "currency": "PLN",
            "description": [purchase.lesson.title for purchase in purchases].join(", "),
            "email": client.user.email,
            "client": f"{client.user.first_name} {client.user.last_name}",
            "urlReturn": f"{FRONTEND_URL}/order-status/?session_id={str(payment.session_id)}",
            "urlStatus": f"{FRONTEND_URL}/api/payment-verify",
            "country": "PL",
            "language": "pl",
            "timeLimit": 5,
            "channel": (1 + 2 + 4 + 8192),
            "waitForResult": False,
            "regulationAccept": True,
            "sign": self._create_register_sign(payment=payment),
        }

        request = requests.post(
            url=self.register_url,
            json=data,
            headers=self.headers,
        )

        response = request.json()
        response_code = response["responseCode"]

        if response_code == 0:
            status_code = status.HTTP_200_OK
            data = {"token": response["data"]["token"]}
        elif response_code == 400:
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": response["error"]}
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
            data = {"error": response["error"]}

        return {"status_code": status_code, "data": data}

    def verify(self, session_id: str, order_id: str, amount: str) -> bool:
        payments = Payment.objects.filter(session_id=session_id, amount=amount)
        if not payments.exists():
            return False

        payment = payments.first()
        payment.order_id = order_id

        data = {
            "merchantId": PAYMENT_MERCHANT_ID,
            "posId": PAYMENT_STORE_ID,
            "sessionId": session_id,
            "amount": amount,
            "currency": "PLN",
            "orderId": order_id,
            "sign": self._create_verify_sign(),
        }

        response = requests.put(self.verify_url, json=data, headers=self.headers)

        if not response.ok:
            return False

        response_data = response.json()
        response_status = response_data["status"]

        if response_status == "success":
            status = "S"
        else:
            status = "F"

        payment.status = status
        payment.save()

        return status == "S"
