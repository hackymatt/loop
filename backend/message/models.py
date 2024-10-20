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

    def add_type(self):
        return self.get_queryset().add_type()


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
