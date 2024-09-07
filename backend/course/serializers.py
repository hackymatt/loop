from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    EmailField,
    IntegerField,
)
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from course.models import Course
from lesson.models import Lesson, Technology, LessonPriceHistory
from topic.models import Topic
from skill.models import Skill
from module.models import Module
from profile.models import Profile, LecturerProfile
from review.models import Review
from purchase.models import Purchase
from teaching.models import Teaching
from django.db.models.functions import Concat
from django.db.models import Sum, Avg, Min, Value
from datetime import timedelta


class VideoBase64File(Base64FileField):
    ALLOWED_TYPES = ["mp4"]

    def get_file_extension(self, filename, decoded_file):
        return "mp4"


def get_course_modules(course):
    course_modules = (
        Course.modules.through.objects.filter(course=course).all().order_by("id")
    )
    return [
        Module.objects.get(id=course_module.module_id)
        for course_module in course_modules
    ]


def get_course_lessons(course):
    course_modules = (
        Course.modules.through.objects.filter(course=course)
        .values("module_id")
        .order_by("id")
    )
    course_lessons = (
        Module.lessons.through.objects.filter(module__in=course_modules)
        .all()
        .order_by("id")
    )
    return [
        Lesson.objects.get(id=course_lesson.lesson_id)
        for course_lesson in course_lessons
    ]


def get_course_skills(course):
    course_skills = (
        Course.skills.through.objects.filter(course=course).all().order_by("id")
    )
    return [
        Skill.objects.get(id=course_skill.skill_id) for course_skill in course_skills
    ]


def get_course_topics(course):
    course_topics = (
        Course.topics.through.objects.filter(course=course).all().order_by("id")
    )
    return [
        Topic.objects.get(id=course_topic.topic_id) for course_topic in course_topics
    ]


def get_price(course_modules):
    lessons_ids = Module.lessons.through.objects.filter(
        module__in=course_modules
    ).values("lesson_id")
    lessons = Lesson.objects.filter(id__in=lessons_ids).all()
    return lessons.aggregate(Sum("price"))["price__sum"]


def get_previous_prices(instance):
    previous_prices = (
        LessonPriceHistory.objects.filter(lesson=instance).order_by("-created_at").all()
    )

    return previous_prices


def get_previous_price(instance):
    current_price = instance.price
    previous_prices = get_previous_prices(instance)

    if previous_prices.count() == 0:
        return None

    last_price_change = previous_prices.first()

    previous_price = last_price_change.price

    if previous_price <= current_price:
        return None

    return previous_price


def get_previous_price_course(course_modules):
    lessons_ids = Module.lessons.through.objects.filter(
        module__in=course_modules
    ).values("lesson_id")
    lessons = Lesson.objects.filter(id__in=lessons_ids).all()
    prices = []
    for lesson in lessons:
        prev = get_previous_price(lesson)
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    previous_price = sum(prices)
    current_price = get_price(course_modules=course_modules)

    if previous_price <= current_price:
        return None

    return previous_price


def get_lowest_30_days_price(instance):
    current_price = instance.price
    previous_prices = get_previous_prices(instance)

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


def get_lowest_30_days_price_course(course_modules):
    lessons_ids = Module.lessons.through.objects.filter(
        module__in=course_modules
    ).values("lesson_id")
    lessons = Lesson.objects.filter(id__in=lessons_ids).all()
    prices = []
    for lesson in lessons:
        prev = get_lowest_30_days_price(lesson)
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    lowest_30_days_price = sum(prices)

    if not get_previous_price_course(course_modules=course_modules):
        return None

    return lowest_30_days_price


def get_lecturers(self, lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = (
        LecturerProfile.objects.filter(id__in=lecturer_ids)
        .annotate(
            full_name=Concat(
                "profile__user__first_name", Value(" "), "profile__user__last_name"
            )
        )
        .order_by("full_name")
    )
    return LecturerSerializer(
        lecturers, many=True, context={"request": self.context.get("request")}
    ).data


def get_technologies(lessons):
    ids = (
        Lesson.technologies.through.objects.filter(lesson__in=lessons)
        .all()
        .order_by("id")
        .all()
        .distinct()
        .values("technology_id")
    )
    technologies = Technology.objects.filter(id__in=ids).all()
    return TechnologySerializer(technologies, many=True).data


def get_lecturers_details(self, lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = (
        LecturerProfile.objects.filter(id__in=lecturer_ids)
        .annotate(
            full_name=Concat(
                "profile__user__first_name", Value(" "), "profile__user__last_name"
            )
        )
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
    course_modules = (
        Course.modules.through.objects.filter(course=course)
        .values("module_id")
        .order_by("id")
    )
    lessons_ids = Module.lessons.through.objects.filter(
        module__in=course_modules
    ).values("lesson_id")
    lessons = Lesson.objects.filter(id__in=lessons_ids).all()
    return lessons.aggregate(Sum("duration"))["duration__sum"]


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
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


class LecturerDetailsSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)
    rating = SerializerMethodField("get_user_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons_count = SerializerMethodField("get_lessons_count")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "email",
            "full_name",
            "gender",
            "title",
            "image",
            "rating",
            "rating_count",
            "lessons_count",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

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


class LessonShortSerializer(ModelSerializer):
    id = IntegerField()
    previous_price = SerializerMethodField("get_lesson_previous_price")
    lowest_30_days_price = SerializerMethodField("get_lesson_lowest_30_days_price")

    def get_lesson_previous_price(self, lesson):
        return get_previous_price(instance=lesson)

    def get_lesson_lowest_30_days_price(self, lesson):
        return get_lowest_30_days_price(instance=lesson)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "price",
            "previous_price",
            "lowest_30_days_price",
        )


class ModuleSerializer(ModelSerializer):
    id = IntegerField()
    price = SerializerMethodField("get_module_price")
    previous_price = SerializerMethodField("get_module_previous_price")
    lowest_30_days_price = SerializerMethodField("get_module_lowest_30_days_price")
    lessons = LessonShortSerializer(many=True)

    def get_module_price(self, module):
        return get_price(course_modules=[module])

    def get_module_previous_price(self, module):
        return get_previous_price_course(course_modules=[module])

    def get_module_lowest_30_days_price(self, module):
        return get_lowest_30_days_price_course(course_modules=[module])

    class Meta:
        model = Module
        fields = (
            "id",
            "title",
            "price",
            "previous_price",
            "lowest_30_days_price",
            "lessons",
        )


class CourseListSerializer(ModelSerializer):
    price = SerializerMethodField("get_course_price")
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    duration = SerializerMethodField("get_course_duration")
    technologies = SerializerMethodField("get_course_technologies")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_course_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_price(course_modules=course_modules)

    def get_course_previous_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_previous_price_course(course_modules=course_modules)

    def get_course_lowest_30_days_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_lowest_30_days_price_course(course_modules=course_modules)

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
            "modules",
            "skills",
            "topics",
            "video",
            "created_at",
            "modified_at",
        )


class CourseGetSerializer(ModelSerializer):
    level = CharField(source="get_level_display")
    price = SerializerMethodField("get_course_price")
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    duration = SerializerMethodField("get_course_duration")
    modules = SerializerMethodField("get_modules")
    technologies = SerializerMethodField("get_course_technologies")
    skills = SerializerMethodField("get_skills")
    topics = SerializerMethodField("get_topics")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    def get_course_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_price(course_modules=course_modules)

    def get_course_previous_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_previous_price_course(course_modules=course_modules)

    def get_course_lowest_30_days_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_lowest_30_days_price_course(course_modules=course_modules)

    def get_course_technologies(self, course):
        lessons = get_course_lessons(course=course)
        return get_technologies(lessons=lessons)

    def get_modules(self, course):
        return ModuleSerializer(get_course_modules(course=course), many=True).data

    def get_skills(self, course):
        return SkillSerializer(get_course_skills(course=course), many=True).data

    def get_topics(self, course):
        return TopicSerializer(get_course_topics(course=course), many=True).data

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
        exclude = (
            "created_at",
            "modified_at",
        )


class CourseSerializer(ModelSerializer):
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    class Meta:
        model = Course
        fields = "__all__"

    def add_modules(self, course, modules):
        for module in modules:
            course.modules.add(module)

        return course

    def add_skills(self, course, skills):
        for skill in skills:
            course.skills.add(skill)

        return course

    def add_topics(self, course, topics):
        for topic in topics:
            course.topics.add(topic)

        return course

    def create(self, validated_data):
        modules = validated_data.pop("modules")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        course = Course.objects.create(**validated_data)
        course = self.add_modules(course=course, modules=modules)
        course = self.add_skills(course=course, skills=skills)
        course = self.add_topics(course=course, topics=topics)
        course.save()

        return course

    def update(self, instance, validated_data):
        modules = validated_data.pop("modules")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        instance.active = validated_data.get("active", instance.active)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.level = validated_data.get("level", instance.level)

        instance.image = validated_data.get("image", instance.image)
        instance.video = validated_data.get("video", instance.video)

        instance.modules.clear()
        instance = self.add_modules(course=instance, modules=modules)
        instance.skills.clear()
        instance = self.add_skills(course=instance, skills=skills)
        instance.topics.clear()
        instance = self.add_topics(course=instance, topics=topics)

        instance.save()

        return instance


class BestCourseSerializer(ModelSerializer):
    price = SerializerMethodField("get_course_price")
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    technologies = SerializerMethodField("get_course_technologies")
    duration = SerializerMethodField("get_course_duration")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_course_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_price(course_modules=course_modules)

    def get_course_previous_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_previous_price_course(course_modules=course_modules)

    def get_course_lowest_30_days_price(self, course):
        course_modules = (
            Course.modules.through.objects.filter(course=course)
            .values("module_id")
            .order_by("id")
        )
        return get_lowest_30_days_price_course(course_modules=course_modules)

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
