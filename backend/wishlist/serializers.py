from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    ListField,
)
from course.models import Course, Lesson, Technology
from wishlist.models import Wishlist
from profile.models import Profile


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


class WishlistGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Wishlist
        exclude = ("profile",)


class WishlistSerializer(ModelSerializer):
    course = IntegerField(required=False)
    lesson = IntegerField(required=False)

    class Meta:
        model = Wishlist
        fields = (
            "course",
            "lesson",
            "profile",
        )

    def create(self, validated_data):
        profile_id = validated_data.pop("profile")
        profile = Profile.objects.get(pk=profile_id)
        course_id = validated_data.get("course", None)
        lesson_id = validated_data.get("lesson", None)

        if course_id:
            course = Course.objects.get(pk=course_id)
            lessons = course.lessons.all()

            wishlist_items = Wishlist.objects.filter(
                lesson__in=lessons, profile=profile
            )

            if wishlist_items.count() == lessons.count():
                wishlist_items.delete()
            else:
                for lesson in lessons:
                    Wishlist.objects.get_or_create(lesson=lesson, profile=profile)

        else:
            lesson = Lesson.objects.get(pk=lesson_id)
            wishlist_item = Wishlist.objects.filter(lesson=lesson, profile=profile)
            if wishlist_item.exists():
                wishlist_item.delete()
            else:
                Wishlist.objects.create(lesson=lesson, profile=profile)

        return Wishlist.objects.filter(profile=profile).all()
