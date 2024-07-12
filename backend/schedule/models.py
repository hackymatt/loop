from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    DateTimeField,
    URLField,
    CASCADE,
    PROTECT,
    Index,
)
from profile.models import LecturerProfile
from lesson.models import Lesson


class Schedule(BaseModel):
    lecturer = ForeignKey(
        LecturerProfile, on_delete=CASCADE, related_name="schedule_lecturer"
    )
    start_time = DateTimeField()
    end_time = DateTimeField()
    lesson = ForeignKey(
        Lesson, on_delete=PROTECT, related_name="schedule_lesson", null=True, blank=True
    )
    meeting_url = URLField(null=True, blank=True)

    class Meta:
        db_table = "schedule"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lecturer", "start_time", "end_time"],
                name="schedule_lecturer_time_unique_together",
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
                    "lesson",
                ]
            ),
            Index(
                fields=[
                    "lesson",
                    "lecturer",
                ]
            ),
        ]
