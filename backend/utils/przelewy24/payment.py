from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
from typing import List
from purchase.models import Purchase, Payment
from profile.models import Profile
import json
import base64


class Przelewy24:
    def __init__(self, payment: Payment) -> None:
        self.register_url = f"{settings.PAYMENT_SERVER}/api/v1/transaction/register"
        self.verify_url = f"{settings.PAYMENT_SERVER}/api/v1/transaction/verify"

        self.payment = payment

        self.auth = HTTPBasicAuth(
            settings.PAYMENT_MERCHANT_ID, settings.PAYMENT_API_KEY
        )

    def _create_sign(self):
        return (
            base64.urlsafe_b64encode(
                json.dumps(
                    {
                        "sessionId": str(self.payment.session_id),
                        "merchantId": settings.PAYMENT_MERCHANT_ID,
                        "amount": self.payment.amount,
                        "currency": "PLN",
                        "crc": settings.PAYMENT_CRC,
                    }
                ).encode()
            ).decode(),
        )

    def register(self, client: Profile, purchases: List[Purchase]):
        data = {
            "merchantId": settings.PAYMENT_MERCHANT_ID,
            "posId": settings.PAYMENT_STORE_ID,
            "sessionId": str(self.payment.session_id),
            "amount": self.payment.amount,
            "currency": "PLN",
            "description": ", ".join([purchase.lesson.title for purchase in purchases]),
            "email": client.user.email,
            "client": f"{client.user.first_name} {client.user.last_name}",
            "country": "PL",
            "language": "pl",
            "method": 0,
            "urlReturn": f"{settings.BASE_FRONTEND_URL}/order-status/",
            "urlStatus": f"{settings.BASE_FRONTEND_URL}/order-status/?id={self.payment.session_id}",
            "timeLimit": 5,
            "channel": 16,
            "waitForResult": False,
            "regulationAccept": True,
            "sign": self._create_sign(),
        }

        request = requests.post(
            url=self.register_url,
            json=data,
            auth=self.auth,
        )
        request.raise_for_status()

        return request

    def verify(self):
        data = {
            "merchantId": settings.PAYMENT_MERCHANT_ID,
            "posId": settings.PAYMENT_STORE_ID,
            "sessionId": str(self.payment.session_id),
            "amount": self.payment.amount,
            "currency": "PLN",
            "orderId": self.payment.order_id,
            "sign": self._create_sign(),
        }

        request = requests.put(
            url=self.register_url,
            json=data,
            auth=self.auth,
        )
        request.raise_for_status()

        return request