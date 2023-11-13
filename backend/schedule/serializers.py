from rest_framework.serializers import ModelSerializer, CharField, EmailField
from schedule.models import Schedule
from profile.models import Profile


class ProfileSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
            "image",
        )


class ScheduleGetSerializer(ModelSerializer):
    lecturer = ProfileSerializer()

    class Meta:
        model = Schedule
        fields = (
            "lecturer",
            "time",
        )


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ("lecturer",)

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        return Schedule.objects.create(**validated_data, lecturer=profile)
