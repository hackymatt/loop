from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    CASCADE,
    Index,
)
from course.models import Lesson
from profile.models import Profile


class Cart(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    student = ForeignKey(Profile, on_delete=CASCADE, related_name="cart_student")

    class Meta:
        db_table = "cart"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "student",
                ]
            ),
            Index(
                fields=[
                    "student",
                    "lesson",
                ]
            ),
        ]
