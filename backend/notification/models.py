from core.base_model import BaseModel
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    Index,
)
from profile.models import Profile


class Notification(BaseModel):
    STATUS_CHOICES = (
        ("N", "NEW"),
        ("R", "READ"),
    )
    profile = ForeignKey(Profile, on_delete=CASCADE)
    title = CharField()
    subtitle = CharField(null=True, blank=True)
    description = TextField()
    status = CharField(choices=STATUS_CHOICES, null=False, default="N")
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
