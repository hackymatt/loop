from core.base_model import BaseModel
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    Index,
)
from profile.models import Profile
from const import StatusType


class Notification(BaseModel):
    profile = ForeignKey(
        Profile, on_delete=CASCADE, related_name="notification_profile"
    )
    title = CharField()
    subtitle = CharField(null=True, blank=True)
    description = TextField()
    status = CharField(choices=StatusType.choices, null=False, default=StatusType.NEW)
    path = CharField(null=True, blank=True)
    icon = CharField()

    class Meta:
        db_table = "notification"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "profile",
                ]
            ),
            Index(
                fields=[
                    "profile",
                    "status",
                ]
            ),
        ]
