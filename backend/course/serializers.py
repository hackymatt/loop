from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    EmailField,
    IntegerField,
)
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from rest_framework.serializers import ValidationError
from course.models import (
    Course,
    Skill,
    Topic,
)
from lesson.models import Lesson, Technology, LessonPriceHistory
from profile.models import Profile
from review.models import Review
from purchase.models import Purchase
from teaching.models import Teaching
from django.db.models.functions import Concat
from django.db.models import Sum, Avg, Min, Value
from django.core.exceptions import FieldDoesNotExist
from datetime import timedelta


class VideoBase64File(Base64FileField):
    ALLOWED_TYPES = ["mp4"]

    def get_file_extension(self, filename, decoded_file):
        return "mp4"


def model_field_exists(obj, field):
    try:
        obj._meta.get_field(field)
        return True
    except (AttributeError, FieldDoesNotExist):
        return False


def get_course_lessons(course):
    return course.lessons.all()


def get_previous_prices(price_history_model, instance):
    if model_field_exists(price_history_model, "course"):
        previous_prices = (
            price_history_model.objects.filter(course=instance)
            .order_by("-created_at")
            .all()
        )
    else:
        previous_prices = (
            price_history_model.objects.filter(lesson=instance)
            .order_by("-created_at")
            .all()
        )

    return previous_prices


def get_previous_price(price_history_model, instance):
    current_price = instance.price
    previous_prices = get_previous_prices(price_history_model, instance)

    if previous_prices.count() == 0:
        return None

    last_price_change = previous_prices.first()

    previous_price = last_price_change.price

    if previous_price <= current_price:
        return None

    return previous_price


def get_lowest_30_days_price(price_history_model, instance):
    current_price = instance.price
    previous_prices = get_previous_prices(price_history_model, instance)

    if previous_prices.count() == 0:
        return None

    last_price_change = previous_prices.first()

    previous_price = last_price_change.price

    if previous_price <= current_price:
        return None

    last_price_change_date = last_price_change.created_at
    last_price_change_date_minus_30_days = last_price_change.created_at - timedelta(
        days=30
    )

    prices_in_last_30_days = previous_prices.filter(
        created_at__lte=last_price_change_date,
        created_at__gte=last_price_change_date_minus_30_days,
    )

    return prices_in_last_30_days.aggregate(Min("price"))["price__min"]


def get_lecturers(self, lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = (
        Profile.objects.filter(id__in=lecturer_ids)
        .annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"))
        .order_by("full_name")
    )
    return LecturerSerializer(
        lecturers, many=True, context={"request": self.context.get("request")}
    ).data


def get_technologies(lessons):
    ids = (
        Lesson.technologies.through.objects.filter(lesson__in=lessons)
        .all()
        .distinct()
        .values("technology_id")
    )
    technologies = Technology.objects.filter(id__in=ids).all()
    return TechnologySerializer(technologies, many=True).data


def get_lecturers_details(self, lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = (
        Profile.objects.filter(id__in=lecturer_ids)
        .annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"))
        .order_by("full_name")
    )
    return LecturerDetailsSerializer(
        lecturers, many=True, context={"request": self.context.get("request")}
    ).data


def get_rating(lessons):
    return Review.objects.filter(lesson__in=lessons).aggregate(Avg("rating"))[
        "rating__avg"
    ]


def get_rating_count(lessons):
    return Review.objects.filter(lesson__in=lessons).count()


def get_students_count(lessons):
    return Purchase.objects.filter(lesson__in=lessons).count()


def get_duration(course):
    return course.lessons.aggregate(Sum("duration"))["duration__sum"]


def get_price(course):
    return course.lessons.aggregate(Sum("price"))["price__sum"]


def get_lecturer_rating(lecturer):
    return Review.objects.filter(lecturer=lecturer)


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        exclude = (
            "modified_at",
            "created_at",
        )


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        exclude = (
            "modified_at",
            "created_at",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="user.email")
    gender = EmailField(source="get_gender_display")
    image = Base64ImageField(required=True)

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "email",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


class LecturerDetailsSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="user.email")
    gender = EmailField(source="get_gender_display")
    rating = SerializerMethodField("get_user_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons_count = SerializerMethodField("get_lessons_count")

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "email",
            "full_name",
            "gender",
            "user_title",
            "image",
            "rating",
            "rating_count",
            "lessons_count",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name

    def get_user_rating(self, lecturer):
        return get_lecturer_rating(lecturer=lecturer).aggregate(Avg("rating"))[
            "rating__avg"
        ]

    def get_lecturer_rating_count(self, lecturer):
        return get_lecturer_rating(lecturer=lecturer).count()

    def get_lessons_count(self, lecturer):
        return (
            Teaching.objects.filter(lecturer=lecturer)
            .values("lesson")
            .distinct()
            .count()
        )


class LessonDetailsSerializer(ModelSerializer):
    id = IntegerField()
    lecturers = SerializerMethodField("get_lesson_lecturers")
    students_count = SerializerMethodField("get_lesson_students_count")
    rating = SerializerMethodField("get_lesson_rating")
    rating_count = SerializerMethodField("get_lesson_rating_count")

    def get_lesson_lecturers(self, lesson):
        return get_lecturers(self, lessons=[lesson])

    def get_lesson_rating(self, lesson):
        return get_rating(lessons=[lesson])

    def get_lesson_rating_count(self, lesson):
        return get_rating_count(lessons=[lesson])

    def get_lesson_students_count(self, lesson):
        return get_students_count(lessons=[lesson])

    class Meta:
        model = Lesson
        exclude = (
            "title",
            "price",
            "created_at",
            "modified_at",
        )


class LessonSerializer(ModelSerializer):
    id = IntegerField()
    technologies = TechnologySerializer(many=True)
    previous_price = SerializerMethodField("get_lesson_previous_price")
    lowest_30_days_price = SerializerMethodField("get_lesson_lowest_30_days_price")
    lecturers = SerializerMethodField("get_lesson_lecturers")
    students_count = SerializerMethodField("get_lesson_students_count")
    rating = SerializerMethodField("get_lesson_rating")
    rating_count = SerializerMethodField("get_lesson_rating_count")

    def get_lesson_previous_price(self, lesson):
        return get_previous_price(
            price_history_model=LessonPriceHistory, instance=lesson
        )

    def get_lesson_lowest_30_days_price(self, lesson):
        return get_lowest_30_days_price(
            price_history_model=LessonPriceHistory, instance=lesson
        )

    def get_lesson_lecturers(self, lesson):
        return get_lecturers(self, lessons=[lesson])

    def get_lesson_rating(self, lesson):
        return get_rating(lessons=[lesson])

    def get_lesson_rating_count(self, lesson):
        return get_rating_count(lessons=[lesson])

    def get_lesson_students_count(self, lesson):
        return get_students_count(lessons=[lesson])

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonShortSerializer(ModelSerializer):
    id = IntegerField()
    previous_price = SerializerMethodField("get_lesson_previous_price")
    lowest_30_days_price = SerializerMethodField("get_lesson_lowest_30_days_price")

    def get_lesson_previous_price(self, lesson):
        return get_previous_price(
            price_history_model=LessonPriceHistory, instance=lesson
        )

    def get_lesson_lowest_30_days_price(self, lesson):
        return get_lowest_30_days_price(
            price_history_model=LessonPriceHistory, instance=lesson
        )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "price",
            "previous_price",
            "lowest_30_days_price",
        )


class CourseListSerializer(ModelSerializer):
    price = SerializerMethodField("get_course_price")
    duration = SerializerMethodField("get_course_duration")
    technologies = SerializerMethodField("get_course_technologies")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_course_price(self, course):
        return get_price(course=course)

    def get_course_technologies(self, course):
        lessons = get_course_lessons(course=course)
        return get_technologies(lessons=lessons)

    def get_course_duration(self, course):
        return get_duration(course=course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers(self, lessons=lessons)

    def get_course_rating(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating(lessons=lessons)

    def get_course_rating_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating_count(lessons=lessons)

    def get_course_students_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_students_count(lessons=lessons)

    class Meta:
        model = Course
        exclude = (
            "lessons",
            "active",
            "skills",
            "topics",
            "video",
            "created_at",
            "modified_at",
        )


class CourseGetSerializer(ModelSerializer):
    level = CharField(source="get_level_display")
    price = SerializerMethodField("get_course_price")
    duration = SerializerMethodField("get_course_duration")
    lessons = SerializerMethodField("get_lessons")
    technologies = SerializerMethodField("get_course_technologies")
    skills = SkillSerializer(many=True)
    topics = TopicSerializer(many=True)
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    def get_course_price(self, course):
        return get_price(course=course)

    def get_course_technologies(self, course):
        lessons = get_course_lessons(course=course)
        return get_technologies(lessons=lessons)

    def get_lessons(self, course):
        return LessonShortSerializer(get_course_lessons(course=course), many=True).data

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers_details(self, lessons=lessons)

    def get_course_rating(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating(lessons=lessons)

    def get_course_rating_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating_count(lessons=lessons)

    def get_course_students_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_students_count(lessons=lessons)

    class Meta:
        model = Course
        exclude = ("active",)


class CourseSerializer(ModelSerializer):
    price = SerializerMethodField("get_course_price")
    duration = SerializerMethodField("get_course_duration")
    lessons = LessonSerializer(many=True)
    technologies = SerializerMethodField("get_course_technologies")
    skills = SkillSerializer(many=True)
    topics = TopicSerializer(many=True)
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    def get_course_price(self, course):
        return get_price(course=course)

    def get_course_technologies(self, course):
        lessons = get_course_lessons(course=course)
        return get_technologies(lessons=lessons)

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers(self, lessons=lessons)

    def get_course_rating(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating(lessons=lessons)

    def get_course_rating_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating_count(lessons=lessons)

    def get_course_students_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_students_count(lessons=lessons)

    class Meta:
        model = Course
        fields = "__all__"

    def validate_lessons(self, lessons):
        if len(lessons) == 0:
            raise ValidationError({"lessons": "Kurs musi posiadać minimum 1 lekcję."})

        return lessons

    def validate_skills(self, skills):
        if len(skills) == 0:
            raise ValidationError(
                {"skills": "Kurs musi posiadać minimum 1 umiejętność."}
            )

        return skills

    def validate_topics(self, topic):
        if len(topic) == 0:
            raise ValidationError(
                {"topic": "Kurs musi posiadać minimum 1 rezultat nauki."}
            )

        return topic

    def add_lessons(self, course, lessons):
        objs = []
        for lesson in lessons:
            obj = Lesson.objects.get(pk=lesson["id"])
            objs.append(obj)

        course.lessons.add(*objs)

        return course

    def add_skills(self, course, skills):
        objs = []
        for skill in skills:
            obj, _ = Skill.objects.get_or_create(name=skill["name"])
            objs.append(obj)

        course.skills.add(*objs)

        return course

    def add_topics(self, course, topics):
        objs = []
        for topic in topics:
            obj, _ = Topic.objects.get_or_create(name=topic["name"])
            objs.append(obj)

        course.topics.add(*objs)

        return course

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        course = Course.objects.create(**validated_data)
        course = self.add_lessons(course=course, lessons=lessons)
        course = self.add_skills(course=course, skills=skills)
        course = self.add_topics(course=course, topics=topics)
        course.save()

        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        instance.active = validated_data.get("active", instance.active)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.level = validated_data.get("level", instance.level)

        instance.lessons.clear()
        instance = self.add_lessons(course=instance, lessons=lessons)
        instance.skills.clear()
        instance = self.add_skills(course=instance, skills=skills)
        instance.topics.clear()
        instance = self.add_topics(course=instance, topics=topics)

        instance.save()

        return instance


class BestCourseSerializer(ModelSerializer):
    price = SerializerMethodField("get_course_price")
    technologies = SerializerMethodField("get_course_technologies")
    duration = SerializerMethodField("get_course_duration")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_course_price(self, course):
        return get_price(course=course)

    def get_course_technologies(self, course):
        lessons = get_course_lessons(course=course)
        return get_technologies(lessons=lessons)

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers(self, lessons=lessons)

    def get_course_rating(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating(lessons=lessons)

    def get_course_rating_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_rating_count(lessons=lessons)

    def get_course_students_count(self, course):
        lessons = get_course_lessons(course=course)
        return get_students_count(lessons=lessons)

    class Meta:
        model = Course
        exclude = (
            "active",
            "skills",
            "topics",
            "video",
            "created_at",
            "modified_at",
            "description",
        )
