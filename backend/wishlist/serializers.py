from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lesson.models import Lesson, Technology
from wishlist.models import Wishlist
from profile.models import LecturerProfile, StudentProfile


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = LecturerProfile
        fields = ("full_name",)

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = ("id", "modified_at", "created_at")


class LessonSerializer(ModelSerializer):
    technologies = TechnologySerializer(many=True)
    lecturers = SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ("id", "title", "duration", "price", "technologies", "lecturers")

    def get_lecturers(self, lesson: Lesson):
        lecturers = LecturerProfile.objects.filter(
            teaching_lecturer__lesson=lesson,
            profile_ready=True,
        ).order_by("full_name")

        return LecturerSerializer(
            lecturers, many=True, context={"request": self.context.get("request")}
        ).data


class WishlistGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Wishlist
        exclude = ("student",)


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ("lesson",)

    def create(self, validated_data):
        user = self.context["request"].user
        student = StudentProfile.objects.get(profile__user=user)
        obj, _ = Wishlist.objects.get_or_create(student=student, **validated_data)
        return obj
