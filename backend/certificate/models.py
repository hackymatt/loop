from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    CASCADE,
    Index,
    BigIntegerField,
    CharField,
    PositiveIntegerField,
    DateTimeField,
    UUIDField,
)
from profile.models import StudentProfile
import uuid


class Certificate(BaseModel):
    TYPE_CHOICES = (
        ("L", "Lekcja"),
        ("M", "Moduł"),
        ("K", "Kurs"),
    )
    uuid = UUIDField(default=uuid.uuid4)
    type = CharField(choices=TYPE_CHOICES, null=False, default="L")
    entity_id = BigIntegerField()
    title = CharField()
    duration = PositiveIntegerField()
    student = ForeignKey(
        StudentProfile, on_delete=CASCADE, related_name="certificate_student"
    )

    class Meta:
        db_table = "certificate"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "student",
                ]
            ),
        ]
