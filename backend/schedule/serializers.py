from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    DateTimeField,
    ListField,
    ValidationError,
)
from schedule.models import Schedule
from profile.models import Profile


TIME_DURATION_MINS = 15


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
    times = ListField(child=DateTimeField())

    class Meta:
        model = Schedule
        exclude = ("time",)

    def validate_times(self, times):
        for time in times:
            if time.minute % TIME_DURATION_MINS != 0:
                raise ValidationError(
                    {
                        "times": f"Czas rozpoczęcia lekcji musi być wielokrotnością {TIME_DURATION_MINS} minut."
                    }
                )

        return times

    @staticmethod
    def is_time_in_list(schedule, times_list):
        schedule_time = schedule.time
        schedule_time_modified = str(schedule_time)[0:19]
        for time in times_list:
            time_modified = time.replace("T", " ")[0:19]
            if time_modified == schedule_time_modified:
                return True

        return False

    def create(self, validated_data):
        lecturer_id = validated_data.pop("lecturer")
        lecturer = Profile.objects.get(pk=lecturer_id)
        times = validated_data.pop("times")

        schedules = Schedule.objects.filter(lecturer=lecturer).all()

        delete_schedules_ids = [
            schedule.id
            for schedule in schedules
            if not self.is_time_in_list(schedule, times)
        ]
        Schedule.objects.filter(id__in=delete_schedules_ids).delete()

        for time in times:
            Schedule.objects.get_or_create(lecturer=lecturer, time=time)

        return Schedule.objects.filter(lecturer=lecturer).all()
