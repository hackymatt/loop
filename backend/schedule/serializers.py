from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ImageField,
)
from schedule.models import Schedule
from schedule.utils import get_min_students_required
from profile.models import LecturerProfile, StudentProfile
from lesson.models import Lesson
from reservation.models import Reservation


def get_students_required(schedule: Schedule, lesson: Lesson = None):
    if not lesson:
        return None

    current_reservations = Reservation.objects.filter(schedule=schedule).count()
    return max(
        get_min_students_required(
            lecturer=schedule.lecturer, lesson=lesson if lesson else schedule.lesson
        )
        - current_reservations,
        0,
    )


class StudentSerializer(ModelSerializer):
    full_name = SerializerMethodField()
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

    def get_full_name(self, student: StudentProfile):
        return student.full_name


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
    students_required = SerializerMethodField()

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

    def get_students(self, schedule: Schedule):
        ids = Reservation.objects.filter(schedule=schedule).values("student")
        students = StudentProfile.objects.filter(id__in=ids).add_full_name().all()
        return StudentSerializer(students, many=True).data

    def get_students_required(self, schedule: Schedule):
        return get_students_required(schedule=schedule)


class ManageScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = (
            "lecturer",
            "lesson",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = LecturerProfile.objects.get(profile__user=user)
        return Schedule.objects.create(lecturer=lecturer, **validated_data)


class ScheduleSerializer(ModelSerializer):
    students_required = SerializerMethodField()

    class Meta:
        model = Schedule
        exclude = (
            "lesson",
            "lecturer",
            "modified_at",
            "created_at",
        )

    def get_students_required(self, schedule: Schedule):
        lesson_id = self.context["request"].query_params.get("lesson_id", None)
        if not lesson_id:
            return None
        lesson = Lesson.objects.get(pk=lesson_id)
        return get_students_required(schedule=schedule, lesson=lesson)


class ScheduleAvailableDateSerializer(ModelSerializer):
    date = SerializerMethodField("get_date")

    class Meta:
        model = Schedule
        fields = ("date",)

    def get_date(self, schedule):
        return schedule["date"]
