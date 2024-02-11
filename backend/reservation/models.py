from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    Index,
)
from profile.models import Profile
from course.models import Lesson
from schedule.models import Schedule


class Reservation(BaseModel):
    student = ForeignKey(Profile, on_delete=CASCADE, related_name="reservation_student")
    lesson = ForeignKey(Lesson, on_delete=CASCADE, related_name="reservation_lesson")
    schedule = ForeignKey(
        Schedule, on_delete=CASCADE, related_name="reservation_schedule"
    )

    class Meta:
        db_table = "reservation"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["student", "schedule"],
                name="reservation_student_lesson_schedule_unique_together",
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
