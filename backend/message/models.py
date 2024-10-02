from core.base_model import BaseModel
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    Index,
)
from profile.models import Profile


class Message(BaseModel):
    STATUS_CHOICES = (
        ("N", "NEW"),
        ("R", "READ"),
    )
    sender = ForeignKey(Profile, on_delete=CASCADE, related_name="message_sender")
    recipient = ForeignKey(Profile, on_delete=CASCADE, related_name="message_recipient")
    subject = CharField()
    body = TextField()
    status = CharField(choices=STATUS_CHOICES, null=False, default="N")

    class Meta:
        db_table = "message"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "sender",
                ]
            ),
            Index(
                fields=[
                    "recipient",
                ]
            ),
            Index(
                fields=[
                    "sender",
                    "recipient",
                ]
            ),
            Index(
                fields=[
                    "status",
                ]
            ),
            Index(
                fields=[
                    "status",
                    "sender",
                    "recipient",
                ]
            ),
        ]
