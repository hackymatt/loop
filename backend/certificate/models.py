from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    CASCADE,
    Index,
    BigIntegerField,
    CharField,
    PositiveIntegerField,
    UUIDField,
    QuerySet,
    Manager,
    Func,
    F,
    ExpressionWrapper,
    DateField,
)
from django.db.models.functions import Cast, TruncDate
from profile.models import StudentProfile
from datetime import timedelta
import uuid


class CertificateQuerySet(QuerySet):
    class ZeroPad(Func):
        function = "LPAD"
        output_field = CharField()  # Set output_field to CharField
        template = "%(function)s(%(expressions)s, 5, '0')"

    def add_reference_number(self):
        return self.annotate(
            reference_number=self.ZeroPad(Cast(F("id"), output_field=CharField()))
        )

    def add_completed_at(self):
        return self.annotate(
            completed_at=TruncDate(
                ExpressionWrapper(
                    F("created_at") - timedelta(days=1), output_field=DateField()
                )
            )
        )


class CertificateManager(Manager):
    def get_queryset(self):
        return CertificateQuerySet(self.model, using=self._db)

    def add_reference_number(self):
        return self.get_queryset().add_reference_number()

    def add_completed_at(self):
        return self.get_queryset().add_completed_at()


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

    objects = CertificateManager()

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
