from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    Index,
)
from lesson.models import Lesson
from profile.models import StudentProfile


class Wishlist(BaseModel):
    student = ForeignKey(
        StudentProfile, on_delete=CASCADE, related_name="wishlist_student"
    )
    lesson = ForeignKey(Lesson, on_delete=CASCADE)

    class Meta:
        db_table = "wishlist"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "student"],
                name="wishlist_lesson_student_unique_together",
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
