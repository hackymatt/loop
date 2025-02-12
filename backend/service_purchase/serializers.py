from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError,
)
from service_purchase.models import Purchase, Payment
from service.models import Service
from django.db.models import Sum


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        exclude = (
            "active",
            "description",
            "price",
            "modified_at",
            "created_at",
        )


class PurchaseGetSerializer(ModelSerializer):
    service = ServiceSerializer()
    payment = SerializerMethodField()

    class Meta:
        model = Purchase
        exclude = (
            "other",
            "modified_at",
        )

    def get_payment(self, purchase: Purchase):
        return Payment.objects.get(id=purchase.payment_id).session_id


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"

    def validate(self, data):
        service = data["service"]
        price = data["price"]
        payment = data["payment"]

        self.validate_payment_amount(price=price, payment=payment)
        self.validate_service(service=service)

        return data

    def validate_payment_amount(self, price, payment: Payment):
        amount = payment.amount / 100
        purchases = Purchase.objects.filter(payment=payment).all()
        total = purchases.aggregate(Sum("price"))["price__sum"] or 0

        if float(total) + float(price) > amount:
            raise ValidationError(
                {"price": "Cena usługi przekracza wartość płatności."}
            )

        return price

    def validate_service(self, service: Service):
        if not service.active:
            raise ValidationError("Usługa jest nieaktywna.")

        return service


class PaymentSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Payment
        exclude = ("modified_at",)

    def create(self, validated_data):
        status = validated_data.pop("get_status_display")

        payment = Payment.objects.create(status=status, **validated_data)

        return payment

    def update(self, instance: Payment, validated_data):
        status = validated_data.pop("get_status_display")

        Payment.objects.filter(pk=instance.pk).update(status=status, **validated_data)

        instance.refresh_from_db()

        return instance
