from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    Index,
)
from lesson.models import Lesson
from profile.models import LecturerProfile


class Teaching(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    lecturer = ForeignKey(
        LecturerProfile, on_delete=CASCADE, related_name="teaching_lecturer"
    )

    class Meta:
        db_table = "teaching"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "lecturer"],
                name="teaching_lesson_lecturer_unique_together",
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
                    "lecturer",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                    "lesson",
                ]
            ),
        ]
