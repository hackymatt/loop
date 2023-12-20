from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    URLField,
    CASCADE,
    Index,
)
from course.models import Lesson
from profile.models import Profile


class Teaching(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    lecturer = ForeignKey(Profile, on_delete=CASCADE, related_name="teaching_lecturer")
    github_url = URLField()

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
