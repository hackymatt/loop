from rest_framework.serializers import ModelSerializer
from profile.models import LecturerProfile


class LecturerProfileDataSerializer(ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = (
            "title",
            "description",
            "linkedin_url",
        )
