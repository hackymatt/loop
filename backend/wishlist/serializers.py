from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    CharField,
    EmailField,
    ListField,
)
from course.models import Course, Lesson, Technology
from wishlist.models import Wishlist
from profile.models import Profile
from schedule.models import Schedule


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    technology = TechnologySerializer()

    class Meta:
        model = Course
        exclude = ("active", "skills", "topics")


class LessonSerializer(ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = "__all__"


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


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("time",)


class WishlistGetSerializer(ModelSerializer):
    lesson = LessonSerializer()
    lecturer = ProfileSerializer()
    time = ScheduleSerializer()

    class Meta:
        model = Wishlist
        exclude = ("student",)


class WishlistSerializer(ModelSerializer):
    wishlist = ListField()

    class Meta:
        model = Wishlist
        fields = (
            "student",
            "wishlist",
        )

    def create(self, validated_data):
        student_id = validated_data.pop("student")
        student = Profile.objects.get(pk=student_id)
        wishlist = validated_data.pop("wishlist")

        for wishlist_item in wishlist:
            lesson_id = wishlist_item["lesson"]
            lecturer_id = wishlist_item["lecturer"]
            time_id = wishlist_item["time"]
            lesson = Lesson.objects.get(pk=lesson_id)
            lecturer = Profile.objects.get(pk=lecturer_id)
            time = Schedule.objects.get(pk=time_id)

            current_lesson = Wishlist.objects.filter(
                student=student, lesson=lesson, lecturer=lecturer, time=time
            )
            if current_lesson.exists():
                current_lesson.delete()
            else:
                Wishlist.objects.filter(student=student, lesson=lesson).all().delete()
                Wishlist.objects.create(
                    student=student, lesson=lesson, lecturer=lecturer, time=time
                )

        return Wishlist.objects.filter(student=student).all()
