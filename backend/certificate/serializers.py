from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    DateField,
)
from certificate.models import Certificate


class CertificateSerializer(ModelSerializer):
    type = CharField(source="get_type_display")
    completed_at = SerializerMethodField()

    class Meta:
        model = Certificate
        fields = (
            "title",
            "type",
            "completed_at",
        )

    def get_completed_at(self, certificate):
        return certificate.completed_at.date()


class CertificateInfoSerializer(ModelSerializer):
    reference_number = SerializerMethodField()
    type = CharField(source="get_type_display")
    completed_at = DateField()
    student_full_name = SerializerMethodField()
    completed_at = SerializerMethodField()

    class Meta:
        model = Certificate
        fields = (
            "reference_number",
            "type",
            "title",
            "duration",
            "completed_at",
            "student_full_name",
        )

    def get_reference_number(self, certificate):
        return "{:05d}".format(certificate.id)

    def get_student_full_name(self, certificate):
        user = certificate.student.profile.user
        return f"{user.first_name} {user.last_name}"

    def get_completed_at(self, certificate):
        return certificate.completed_at.date()
