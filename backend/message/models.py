from core.base_model import BaseModel
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    Index,
    QuerySet,
    Manager,
    Case,
    When,
    Value,
    F,
)
from profile.models import Profile
from const import StatusType


class MessageQuerySet(QuerySet):
    def add_type(self):
        return self.annotate(
            type=Case(
                When(profile_id=F("recipient__id"), then=Value("INBOX")),
                default=Value("SENT"),
                output_field=CharField(),
            )
        )


class MessageManager(Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)


class Message(BaseModel):
    sender = ForeignKey(Profile, on_delete=CASCADE, related_name="message_sender")
    recipient = ForeignKey(Profile, on_delete=CASCADE, related_name="message_recipient")
    subject = CharField()
    body = TextField()
    status = CharField(choices=StatusType.choices, null=False, default=StatusType.NEW)

    objects = MessageManager()

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
