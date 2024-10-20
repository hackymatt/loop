from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    DateField,
    UUIDField,
)
from certificate.models import Certificate


class CertificateSerializer(ModelSerializer):
    id = UUIDField(source="uuid")
    type = CharField(source="get_type_display")
    completed_at = SerializerMethodField()

    class Meta:
        model = Certificate
        fields = (
            "id",
            "title",
            "type",
            "completed_at",
        )

    def get_completed_at(self, certificate: Certificate):
        return certificate.completed_at


class CertificateInfoSerializer(ModelSerializer):
    id = UUIDField(source="uuid")
    reference_number = SerializerMethodField()
    type = CharField(source="get_type_display")
    student_full_name = SerializerMethodField()
    completed_at = SerializerMethodField()

    class Meta:
        model = Certificate
        fields = (
            "id",
            "reference_number",
            "type",
            "title",
            "duration",
            "completed_at",
            "student_full_name",
        )

    def get_reference_number(self, certificate: Certificate):
        return certificate.reference_number

    def get_student_full_name(self, certificate: Certificate):
        return certificate.student.full_name

    def get_completed_at(self, certificate: Certificate):
        return certificate.completed_at
