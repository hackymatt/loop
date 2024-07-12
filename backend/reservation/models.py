from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    PROTECT,
    Index,
)
from profile.models import StudentProfile
from course.models import Lesson
from schedule.models import Schedule
from purchase.models import Purchase


class Reservation(BaseModel):
    student = ForeignKey(
        StudentProfile, on_delete=CASCADE, related_name="reservation_student"
    )
    lesson = ForeignKey(Lesson, on_delete=PROTECT, related_name="reservation_lesson")
    schedule = ForeignKey(
        Schedule, on_delete=CASCADE, related_name="reservation_schedule"
    )
    purchase = ForeignKey(
        Purchase, on_delete=CASCADE, related_name="reservation_purchase"
    )

    class Meta:
        db_table = "reservation"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["student", "lesson", "schedule", "purchase"],
                name="reservation_student_lesson_schedule_purchase_unique_together",
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
                    "schedule",
                ]
            ),
            Index(
                fields=[
                    "purchase",
                ]
            ),
            Index(
                fields=[
                    "student",
                    "lesson",
                ]
            ),
        ]
