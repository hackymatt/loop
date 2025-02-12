from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from service_purchase.serializers import (
    PurchaseGetSerializer,
    PurchaseSerializer,
    PaymentSerializer,
)
from service_purchase.models import Purchase, Payment
from service_purchase.filters import PurchaseFilter, PaymentFilter
from purchase.utils import Invoice
from mailer.mailer import Mailer
from config_global import CONTACT_EMAIL, ACCOUNT_NUMBER
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


def confirm_purchase(purchases, payment: Payment):
    payment_successful = payment.status == "S"
    payment_rejected = payment.status == "F"

    amount = payment.amount / 100
    currency = payment.currency

    purchase = purchases[0]

    mailer = Mailer()
    mail_data = {
        **{
            "title": "Płatność utworzona",
            "description": "Poniżej przedstawione szczegóły zakupu.",
            "lessons": [purchase.service.title for purchase in purchases],
            "amount": f"{amount:,.2f} {currency}",
            "status": "Utworzona",
        }
    }

    attachments = []

    customer = {
        "id": purchase.other.id,
        "full_name": f"{purchase.other.profile.user.first_name} {purchase.other.profile.user.last_name}",
        "street_address": purchase.other.profile.street_address,
        "city": purchase.other.profile.city,
        "zip_code": purchase.other.profile.zip_code,
        "country": purchase.other.profile.country,
    }
    items = [
        {
            "id": purchase.service.id,
            "name": purchase.service.title,
            "price": purchase.service.price,
        }
        for purchase in purchases
    ]
    notes = payment.notes
    payment = {
        "id": payment.id,
        "amount": payment.amount / 100,
        "currency": payment.currency,
        "status": "Zapłacono" if payment_successful else "Do zapłaty",
        "method": payment.method,
        "account": ACCOUNT_NUMBER if payment.method == "Przelew" else None,
    }
    invoice = Invoice(customer=customer, items=items, payment=payment, notes=notes)
    if not payment_rejected:
        invoice_path = invoice.create()
        attachments = [invoice_path]
        invoice.upload()

    mailer.send(
        email_template="purchase_confirmation.html",
        to=[CONTACT_EMAIL],
        subject="Podsumowanie zakupu",
        data=mail_data,
        attachments=attachments,
    )

    if not payment_rejected:
        invoice.remove()


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Purchase.objects.all().order_by("id")
    serializer_class = PurchaseSerializer
    filterset_class = PurchaseFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PurchaseGetSerializer
        return self.serializer_class


class PaymentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Payment.objects.all().order_by("id")
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated, IsAdminUser]


@receiver([post_save], sender=Purchase)
def check_total_purchase_amount(sender, instance: Purchase, **kwargs):
    payment = instance.payment
    purchases = Purchase.objects.filter(payment=payment)

    total_price = purchases.aggregate(Sum("price"))["price__sum"]

    if total_price == payment.amount / 100:
        confirm_purchase(purchases=purchases, payment=payment)
