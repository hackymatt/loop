from core.base_model import BaseModel
from django.db.models import (
    CharField,
    TextField,
    BooleanField,
    DecimalField,
    Index,
)
from django.core.validators import MinValueValidator
from decimal import Decimal


class Service(BaseModel):
    title = CharField()
    description = TextField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    active = BooleanField(default=False)

    class Meta:
        db_table = "service"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]
