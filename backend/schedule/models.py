from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    DateTimeField,
    CASCADE,
    Index,
)
from profile.models import Profile


class Schedule(BaseModel):
    lecturer = ForeignKey(Profile, on_delete=CASCADE, related_name="schedule_lecturer")
    time = DateTimeField()

    class Meta:
        db_table = "schedule"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lecturer", "time"],
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
        ]
