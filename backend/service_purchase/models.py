from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    DecimalField,
    UUIDField,
    BigIntegerField,
    IntegerField,
    CharField,
    TextField,
    SET,
    PROTECT,
    Index,
)
from service.models import Service
from profile.models import OtherProfile
from config_global import DUMMY_OTHER_EMAIL
import uuid


def get_dummy_other_profile():
    return OtherProfile.objects.get(profile__user__email=DUMMY_OTHER_EMAIL)


class Payment(BaseModel):
    STATUS_CHOICES = (
        ("P", "Pending"),
        ("S", "Success"),
        ("F", "Failure"),
    )
    CURRENCY_CHOICES = (
        ("PLN", "PLN"),
        ("EUR", "EUR"),
        ("USD", "USD"),
    )
    METHOD_CHOICES = (
        ("Przelewy24", "Przelewy24"),
        ("PayPal", "PayPal"),
        ("Przelew", "Przelew"),
    )
    session_id = UUIDField(default=uuid.uuid4)
    order_id = BigIntegerField(null=True, default=None)
    amount = IntegerField()
    currency = CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")
    method = CharField(
        max_length=max(len(choice[0]) for choice in METHOD_CHOICES),
        choices=METHOD_CHOICES,
        default="Przelew",
    )
    status = CharField(choices=STATUS_CHOICES, default="P")
    notes = TextField()

    class Meta:
        db_table = "service_payment"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "session_id",
                ]
            ),
            Index(
                fields=[
                    "order_id",
                ]
            ),
        ]


class Purchase(BaseModel):
    service = ForeignKey(
        Service,
        on_delete=PROTECT,
        related_name="purchase_service",
    )
    other = ForeignKey(
        OtherProfile,
        on_delete=SET(get_dummy_other_profile),
        related_name="purchase_other",
    )
    price = DecimalField(max_digits=7, decimal_places=2, null=True)
    payment = ForeignKey(Payment, on_delete=PROTECT, related_name="purchase_payment")

    class Meta:
        db_table = "service_purchase"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "service",
                ]
            ),
            Index(
                fields=[
                    "other",
                    "service",
                ]
            ),
        ]
