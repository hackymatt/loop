from django.db.models import (
    Model,
    UniqueConstraint,
    ForeignKey,
    DateTimeField,
    DecimalField,
    CASCADE,
    Index,
)
from course.models import Lesson
from profile.models import Profile
from schedule.models import Schedule


class Purchase(Model):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    student = ForeignKey(Profile, on_delete=CASCADE, related_name="purchase_student")
    lecturer = ForeignKey(Profile, on_delete=CASCADE, related_name="purchase_lecturer")
    time = ForeignKey(Schedule, on_delete=CASCADE)
    price = DecimalField(max_digits=7, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "purchase"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "student", "lecturer"],
                name="purchase_lesson_student_lecturer_unique_together",
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
                    "lesson",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                ]
            ),
            Index(
                fields=[
                    "student",
                    "lesson",
                    "lecturer",
                ]
            ),
        ]
