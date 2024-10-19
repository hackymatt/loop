from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    OneToOneField,
    ForeignKey,
    DateTimeField,
    CharField,
    URLField,
    CASCADE,
    PROTECT,
    Index,
)
from profile.models import LecturerProfile
from lesson.models import Lesson


class Meeting(BaseModel):
    event_id = CharField(unique=True)
    url = URLField()

    class Meta:
        db_table = "meeting"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "event_id",
                ]
            ),
            Index(
                fields=[
                    "url",
                ]
            ),
        ]


class Schedule(BaseModel):
    lecturer = ForeignKey(
        LecturerProfile, on_delete=CASCADE, related_name="schedule_lecturer"
    )
    start_time = DateTimeField()
    end_time = DateTimeField()
    lesson = ForeignKey(
        Lesson, on_delete=PROTECT, related_name="schedule_lesson", null=True, blank=True
    )
    meeting = OneToOneField(Meeting, on_delete=CASCADE, null=True, blank=True)

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


class Recording(BaseModel):
    schedule = ForeignKey(
        Schedule, on_delete=CASCADE, related_name="recording_schedule"
    )
    file_id = CharField()
    file_name = CharField()
    file_url = URLField()

    class Meta:
        db_table = "recording"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "file_id",
                ]
            ),
            Index(
                fields=[
                    "file_name",
                ]
            ),
        ]
