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
        self.validate_service(data["service"])
        self.validate_price(data["price"], data["payment"])

        return data

    def validate_service(self, service: Service):
        if not service.active:
            raise ValidationError("Usługa jest nieaktywna.")

        return service

    def validate_price(self, price: float, payment: Payment):
        payment = Payment.objects.get(id=payment)
        amount = payment.amount / 100
        purchases = Purchase.objects.filter(payment=payment).all()
        total = purchases.aggregate(Sum("price"))["price__sum"]

        if total + price > amount:
            raise ValidationError("Cena usługi przekracza wartość płatności.")

        return price


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
