from django.db.models import (
    Model,
    CharField,
    TextField,
    PositiveIntegerField,
    URLField,
    DecimalField,
)
from django.core.validators import MinValueValidator
from decimal import Decimal


class Lesson(Model):
    title = CharField()
    description = TextField()
    duration = PositiveIntegerField()
    github_branch_link = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "lesson"
