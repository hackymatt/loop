from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    Index,
)
from course.models import Lesson
from profile.models import Profile
from schedule.models import Schedule


class Cart(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    student = ForeignKey(Profile, on_delete=CASCADE, related_name="cart_student")

    class Meta:
        db_table = "cart"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "student"],
                name="cart_lesson_student_unique_together",
            )
        ]
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
