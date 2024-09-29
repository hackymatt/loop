from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ImageField,
)
from schedule.models import Schedule
from schedule.utils import get_min_students_required
from profile.models import Profile, LecturerProfile, StudentProfile
from lesson.models import Lesson
from reservation.models import Reservation


class StudentSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = StudentProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, student):
        return student.profile.user.first_name + " " + student.profile.user.last_name


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
        )


class ManageScheduleGetSerializer(ModelSerializer):
    lesson = LessonSerializer()
    meeting_url = SerializerMethodField()
    students = SerializerMethodField()
    students_required = SerializerMethodField("get_students_required")

    class Meta:
        model = Schedule
        exclude = (
            "meeting",
            "lecturer",
            "modified_at",
            "created_at",
        )

    def get_meeting_url(self, schedule):
        if schedule.meeting:
            return schedule.meeting.url
        return None

    def get_students(self, schedule):
        ids = Reservation.objects.filter(schedule=schedule).values("student")
        students = StudentProfile.objects.filter(id__in=ids).all()
        return StudentSerializer(students, many=True).data

    def get_students_required(self, schedule):
        if not schedule.lesson:
            return None
        return max(
            get_min_students_required(
                lecturer=schedule.lecturer, lesson=schedule.lesson
            )
            - Reservation.objects.filter(schedule=schedule).count(),
            0,
        )


class ManageScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = (
            "lecturer",
            "lesson",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = LecturerProfile.objects.get(profile=Profile.objects.get(user=user))

        return Schedule.objects.create(lecturer=lecturer, **validated_data)


class ScheduleSerializer(ModelSerializer):
    students_required = SerializerMethodField("get_students_required")

    class Meta:
        model = Schedule
        exclude = (
            "lesson",
            "lecturer",
            "modified_at",
            "created_at",
        )

    def get_students_required(self, schedule):
        lesson_id = self.context["request"].query_params.get("lesson_id")
        lessons = Lesson.objects.filter(pk=lesson_id).all()
        if not lessons.exists():
            return None

        return max(
            get_min_students_required(
                lecturer=schedule.lecturer, lesson=lessons.first()
            )
            - Reservation.objects.filter(schedule=schedule).count(),
            0,
        )


class ScheduleAvailableDateSerializer(ModelSerializer):
    date = SerializerMethodField("get_date")

    class Meta:
        model = Schedule
        fields = ("date",)

    def get_date(self, schedule):
        return schedule["date"]
