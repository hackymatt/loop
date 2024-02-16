from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    DecimalField,
    CASCADE,
    PROTECT,
    Index,
)
from lesson.models import Lesson
from profile.models import Profile


class Purchase(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=PROTECT)
    student = ForeignKey(
        Profile, on_delete=CASCADE, related_name="lesson_purchase_student"
    )
    price = DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        db_table = "purchase"
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
            Index(
                fields=[
                    "student",
                    "lesson",
                ]
            ),
        ]
