from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    CharField,
    IntegerField,
    DecimalField,
    CASCADE,
    Index,
)
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from decimal import Decimal
from profile.models import Profile


class Finance(BaseModel):
    lecturer = ForeignKey(Profile, on_delete=CASCADE, related_name="finance_lecturer")
    account = CharField(max_length=26, validators=[MinLengthValidator(26)], null=True)
    commission = IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)], null=True
    )
    rate = DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
    )

    class Meta:
        db_table = "finance"
        ordering = ["lecturer"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                ]
            ),
        ]


class FinanceHistory(BaseModel):
    lecturer = ForeignKey(
        Profile, on_delete=CASCADE, related_name="finance_history_lecturer"
    )
    account = CharField(max_length=26, validators=[MinLengthValidator(26)], null=True)
    commission = IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)], null=True
    )
    rate = DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
    )

    class Meta:
        db_table = "finance_history"
        ordering = ["lecturer"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                ]
            ),
        ]
