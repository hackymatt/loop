from django.db.models import (
    Model,
    EmailField,
    UUIDField,
    BooleanField,
    Index,
)
import uuid


class Newsletter(Model):
    email = EmailField()
    uuid = UUIDField(default=uuid.uuid4)
    active = BooleanField(default=True)

    class Meta:
        db_table = "newsletter"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "uuid",
                ]
            ),
        ]
