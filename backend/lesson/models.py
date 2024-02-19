from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    CharField,
    TextField,
    BooleanField,
    PositiveIntegerField,
    URLField,
    DecimalField,
    ManyToManyField,
    CASCADE,
    Index,
)
from django.core.validators import MinValueValidator
from decimal import Decimal


class Technology(BaseModel):
    name = CharField()

    class Meta:
        db_table = "technology"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "name",
                ]
            ),
        ]


class Lesson(BaseModel):
    title = CharField()
    description = TextField()
    technologies = ManyToManyField(Technology, related_name="lesson_technologies")
    duration = PositiveIntegerField()
    github_url = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    active = BooleanField(default=False)

    class Meta:
        db_table = "lesson"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]


class LessonPriceHistory(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "lesson_price_history"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "lesson",
                ]
            ),
        ]
