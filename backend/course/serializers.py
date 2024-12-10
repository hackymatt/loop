from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    IntegerField,
)
from django.db.models import Case, When, IntegerField
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from course.models import Course
from lesson.models import Lesson, Technology
from topic.models import Topic
from candidate.models import Candidate
from tag.models import Tag
from module.models import Module
from profile.models import LecturerProfile, StudentProfile
from notification.utils import notify
from urllib.parse import quote_plus
from math import ceil


class VideoBase64File(Base64FileField):
    ALLOWED_TYPES = ["mp4"]

    def get_file_extension(self, filename, decoded_file):
        return "mp4"


def notify_students(course: Course):
    students = StudentProfile.objects.all()
    for student in students:
        path = quote_plus(f"{course.title.lower()}-{course.id}")
        notify(
            profile=student.profile,
            title="Nowy kurs w ofercie",
            subtitle=course.title,
            description="Właśnie dodaliśmy nowy kurs. Sprawdź go już teraz.",
            path=f"/course/{path}",
            icon="mdi:account-student",
        )


def format_rating(value):
    if value is None:
        return None
    return ceil(value * 10) / 10


def get_previous_price_course(course: Course):
    lessons = Lesson.objects.filter(id__in=course.lessons).add_previous_price().all()
    prices = []
    for lesson in lessons:
        prev = lesson.previous_price
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    previous_price = sum(prices)
    current_price = course.price

    if previous_price <= current_price:
        return None

    return previous_price


def get_previous_price_module(module: Module):
    lessons = (
        Lesson.objects.filter(id__in=module.lessons.all()).add_previous_price().all()
    )
    prices = []
    for lesson in lessons:
        prev = lesson.previous_price
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    previous_price = sum(prices)
    current_price = module.price

    if previous_price <= current_price:
        return None

    return previous_price


def get_lowest_30_days_price_course(course: Course):
    lessons = (
        Lesson.objects.filter(id__in=course.lessons).add_lowest_30_days_price().all()
    )
    prices = []
    for lesson in lessons:
        prev = lesson.lowest_30_days_price
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    lowest_30_days_price = sum(prices)

    if not get_previous_price_course(course=course):
        return None

    return lowest_30_days_price


def get_lowest_30_days_price_module(module: Module):
    lessons = (
        Lesson.objects.filter(id__in=module.lessons.all())
        .add_lowest_30_days_price()
        .all()
    )
    prices = []
    for lesson in lessons:
        prev = lesson.lowest_30_days_price
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    lowest_30_days_price = sum(prices)

    if not get_previous_price_module(module=module):
        return None

    return lowest_30_days_price


def get_lecturers_info(self, course: Course):
    lecturers = (
        LecturerProfile.objects.add_profile_ready()
        .filter(id__in=course.lecturers_ids, profile_ready=True)
        .add_full_name()
        .order_by("full_name")
    )
    return LecturerSerializer(
        lecturers, many=True, context={"request": self.context.get("request")}
    ).data


def get_technologies(course: Course):
    technologies = Technology.objects.filter(name__in=course.technologies_names).all()
    return TechnologySerializer(technologies, many=True).data


def get_lecturers_details(self, course: Course):
    lecturers = (
        LecturerProfile.objects.add_profile_ready()
        .filter(id__in=course.lecturers_ids, profile_ready=True)
        .add_full_name()
        .add_rating()
        .add_rating_count()
        .add_lessons_count()
        .order_by("full_name")
    )
    return LecturerDetailsSerializer(
        lecturers, many=True, context={"request": self.context.get("request")}
    ).data


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
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


class CandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        exclude = (
            "modified_at",
            "created_at",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class LecturerDetailsSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    lessons_count = SerializerMethodField()

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "title",
            "image",
            "rating",
            "rating_count",
            "lessons_count",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name

    def get_rating(self, lecturer: LecturerProfile):
        return format_rating(lecturer.rating)

    def get_rating_count(self, lecturer: LecturerProfile):
        return lecturer.rating_count

    def get_lessons_count(self, lecturer: LecturerProfile):
        return lecturer.lessons_count


class LessonSerializer(ModelSerializer):
    id = IntegerField()
    previous_price = SerializerMethodField()
    lowest_30_days_price = SerializerMethodField()
    progress = SerializerMethodField()

    def get_previous_price(self, lesson: Lesson):
        return lesson.previous_price

    def get_lowest_30_days_price(self, lesson: Lesson):
        return lesson.lowest_30_days_price

    def get_progress(self, lesson: Lesson):
        return lesson.progress

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "price",
            "previous_price",
            "lowest_30_days_price",
            "progress",
        )


class ModuleSerializer(ModelSerializer):
    id = IntegerField()
    price = SerializerMethodField()
    previous_price = SerializerMethodField()
    lowest_30_days_price = SerializerMethodField()
    lessons = SerializerMethodField()
    progress = SerializerMethodField()

    def get_price(self, module: Module):
        return module.price

    def get_previous_price(self, module: Module):
        return get_previous_price_module(module=module)

    def get_lowest_30_days_price(self, module: Module):
        return get_lowest_30_days_price_module(module=module)

    def get_lessons(self, module: Module):
        lessons = (
            module.lessons.add_progress(user=self.context["request"].user)
            .add_previous_price()
            .add_lowest_30_days_price()
            .all()
        )
        return LessonSerializer(
            lessons, many=True, context={"request": self.context.get("request")}
        ).data

    def get_progress(self, module: Module):
        return module.progress

    class Meta:
        model = Module
        fields = (
            "id",
            "title",
            "price",
            "previous_price",
            "lowest_30_days_price",
            "lessons",
            "progress",
        )


class CourseListSerializer(ModelSerializer):
    price = SerializerMethodField()
    previous_price = SerializerMethodField()
    lowest_30_days_price = SerializerMethodField()
    duration = SerializerMethodField()
    technologies = SerializerMethodField()
    lecturers = SerializerMethodField()
    students_count = SerializerMethodField()
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    progress = SerializerMethodField()
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_price(self, course: Course):
        return course.price

    def get_previous_price(self, course: Course):
        return get_previous_price_course(course=course)

    def get_lowest_30_days_price(self, course: Course):
        return get_lowest_30_days_price_course(course=course)

    def get_technologies(self, course: Course):
        return get_technologies(course=course)

    def get_duration(self, course):
        return course.duration

    def get_lecturers(self, course: Course):
        return get_lecturers_info(self, course=course)

    def get_rating(self, course: Course):
        return format_rating(course.rating)

    def get_rating_count(self, course: Course):
        return course.rating_count

    def get_students_count(self, course: Course):
        return course.students_count

    def get_progress(self, course):
        return course.progress

    class Meta:
        model = Course
        exclude = (
            "modules",
            "tags",
            "topics",
            "candidates",
            "video",
            "overview",
            "created_at",
            "modified_at",
        )


class CourseGetSerializer(ModelSerializer):
    level = CharField(source="get_level_display")
    price = SerializerMethodField()
    previous_price = SerializerMethodField()
    lowest_30_days_price = SerializerMethodField()
    duration = SerializerMethodField()
    modules = SerializerMethodField()
    technologies = SerializerMethodField()
    tags = SerializerMethodField()
    topics = SerializerMethodField()
    candidates = SerializerMethodField()
    lecturers = SerializerMethodField()
    students_count = SerializerMethodField()
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    progress = SerializerMethodField()
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    def get_price(self, course: Course):
        return course.price

    def get_previous_price(self, course: Course):
        return get_previous_price_course(course=course)

    def get_lowest_30_days_price(self, course: Course):
        return get_lowest_30_days_price_course(course=course)

    def get_technologies(self, course: Course):
        return get_technologies(course=course)

    def get_modules(self, course: Course):
        module_ids = list(
            Course.modules.through.objects.filter(course=course)
            .order_by("id")
            .values_list("module_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(module_ids)],
            output_field=IntegerField(),
        )
        modules = (
            Module.objects.add_price()
            .add_progress(user=self.context["request"].user)
            .filter(id__in=module_ids)
            .order_by(preserved_order)
        )

        return ModuleSerializer(
            modules,
            many=True,
            context={"request": self.context.get("request")},
        ).data

    def get_tags(self, course: Course):
        tag_ids = list(
            Course.tags.through.objects.filter(course=course)
            .order_by("id")
            .values_list("tag_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(tag_ids)],
            output_field=IntegerField(),
        )
        tags = Tag.objects.filter(id__in=tag_ids).order_by(preserved_order)
        return TagSerializer(tags, many=True).data

    def get_topics(self, course: Course):
        topic_ids = list(
            Course.topics.through.objects.filter(course=course)
            .order_by("id")
            .values_list("topic_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(topic_ids)],
            output_field=IntegerField(),
        )
        topics = Topic.objects.filter(id__in=topic_ids).order_by(preserved_order)
        return TopicSerializer(topics, many=True).data

    def get_candidates(self, course: Course):
        candidate_ids = list(
            Course.candidates.through.objects.filter(course=course)
            .order_by("id")
            .values_list("candidate_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(candidate_ids)],
            output_field=IntegerField(),
        )
        candidates = Candidate.objects.filter(id__in=candidate_ids).order_by(
            preserved_order
        )
        return CandidateSerializer(candidates, many=True).data

    def get_duration(self, course: Course):
        return course.duration

    def get_lecturers(self, course: Course):
        return get_lecturers_details(self, course=course)

    def get_rating(self, course: Course):
        return format_rating(course.rating)

    def get_rating_count(self, course: Course):
        return course.rating_count

    def get_students_count(self, course: Course):
        return course.students_count

    def get_progress(self, course: Course):
        return course.progress

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

    def add_modules(self, course: Course, modules):
        for module in modules:
            course.modules.add(module)

        return course

    def add_tags(self, course: Course, tags):
        names = [tag.name for tag in tags]
        existing_names = set(
            Tag.objects.filter(name__in=names).values_list("name", flat=True)
        )

        missing_tags = [Tag(name=name) for name in set(names) - existing_names]

        Tag.objects.bulk_create(missing_tags, ignore_conflicts=True)

        tags_objs = Tag.objects.filter(name__in=names)

        for tags_obj in tags_objs:
            course.tags.add(tags_obj)

        return course

    def add_topics(self, course: Course, topics):
        names = [topic.name for topic in topics]
        existing_names = set(
            Topic.objects.filter(name__in=names).values_list("name", flat=True)
        )

        missing_topics = [Topic(name=name) for name in set(names) - existing_names]

        Topic.objects.bulk_create(missing_topics, ignore_conflicts=True)

        topics_objs = Topic.objects.filter(name__in=names)

        for topics_obj in topics_objs:
            course.topics.add(topics_obj)

        return course

    def add_candidates(self, course: Course, candidates):
        names = [candidate.name for candidate in candidates]
        existing_names = set(
            Candidate.objects.filter(name__in=names).values_list("name", flat=True)
        )

        missing_candidates = [
            Candidate(name=name) for name in set(names) - existing_names
        ]

        Candidate.objects.bulk_create(missing_candidates, ignore_conflicts=True)

        candidates_objs = Candidate.objects.filter(name__in=names)

        for candidates_obj in candidates_objs:
            course.candidates.add(candidates_obj)

        return course

    def create(self, validated_data):
        modules = validated_data.pop("modules")
        tags = validated_data.pop("tags")
        topics = validated_data.pop("topics")
        candidates = validated_data.pop("candidates")

        course = Course.objects.create(**validated_data)
        course = self.add_modules(course=course, modules=modules)
        course = self.add_tags(course=course, tags=tags)
        course = self.add_topics(course=course, topics=topics)
        course = self.add_candidates(course=course, candidates=candidates)
        course.save()

        if course.active:
            notify_students(course=course)

        return course

    def update(self, instance: Course, validated_data):
        modules = validated_data.pop("modules")
        tags = validated_data.pop("tags")
        topics = validated_data.pop("topics")
        candidates = validated_data.pop("candidates")

        instance.active = validated_data.get("active", instance.active)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.overview = validated_data.get("overview", instance.overview)
        instance.level = validated_data.get("level", instance.level)

        instance.image = validated_data.get("image", instance.image)
        instance.video = validated_data.get("video", instance.video)

        instance.modules.clear()
        instance = self.add_modules(course=instance, modules=modules)
        instance.tags.clear()
        instance = self.add_tags(course=instance, tags=tags)
        instance.topics.clear()
        instance = self.add_topics(course=instance, topics=topics)
        instance.candidates.clear()
        course = self.add_candidates(course=instance, candidates=candidates)

        instance.save()

        if instance.active:
            notify_students(course=instance)

        return instance


class BestCourseSerializer(ModelSerializer):
    price = SerializerMethodField()
    previous_price = SerializerMethodField()
    lowest_30_days_price = SerializerMethodField()
    technologies = SerializerMethodField()
    duration = SerializerMethodField()
    lecturers = SerializerMethodField()
    students_count = SerializerMethodField()
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_price(self, course: Course):
        return course.price

    def get_previous_price(self, course: Course):
        return get_previous_price_course(course=course)

    def get_lowest_30_days_price(self, course: Course):
        return get_lowest_30_days_price_course(course=course)

    def get_technologies(self, course: Course):
        return get_technologies(course=course)

    def get_duration(self, course):
        return course.duration

    def get_lecturers(self, course: Course):
        return get_lecturers_info(self, course=course)

    def get_rating(self, course: Course):
        return format_rating(course.rating)

    def get_rating_count(self, course: Course):
        return course.rating_count

    def get_students_count(self, course: Course):
        return course.students_count

    class Meta:
        model = Course
        exclude = (
            "active",
            "tags",
            "topics",
            "candidates",
            "video",
            "created_at",
            "modified_at",
            "description",
            "overview",
        )
