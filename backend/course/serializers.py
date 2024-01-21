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
    Lesson,
    Course,
    Technology,
    Skill,
    Topic,
    LessonPriceHistory,
    CoursePriceHistory,
)
from profile.models import Profile
from review.models import Review
from purchase.models import LessonPurchase
from teaching.models import Teaching
from django.db.models import Sum, Avg, Min, Count
from django.core.exceptions import FieldDoesNotExist
from datetime import timedelta


MIN_LESSON_DURATION_MINS = 15


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


def get_course_lessons(course, active=True):
    return Lesson.objects.filter(course=course, active=active).all()


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


def get_lecturers(lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = Profile.objects.filter(id__in=lecturer_ids).order_by("uuid")
    return LecturerSerializer(lecturers, many=True).data


def get_lecturers_details(lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = Profile.objects.filter(id__in=lecturer_ids).order_by("uuid")
    return LecturerDetailsSerializer(lecturers, many=True).data


def get_rating(lessons):
    return Review.objects.filter(lesson__in=lessons).aggregate(Avg("rating"))[
        "rating__avg"
    ]


def get_rating_count(lessons):
    return Review.objects.filter(lesson__in=lessons).count()


def get_students_count(lessons):
    return LessonPurchase.objects.filter(lesson__in=lessons).count()


def get_duration(course):
    return Lesson.objects.filter(course=course).aggregate(Sum("duration"))[
        "duration__sum"
    ]


def get_lecturer_rating(lecturer):
    return Review.objects.filter(lecturer=lecturer)


def get_is_bestseller(lesson):
    course = lesson.course
    lessons = course.lessons.all()

    students_count = (
        LessonPurchase.objects.filter(lesson__in=lessons)
        .values("lesson__pk")
        .annotate(count=Count("student"))
        .order_by("-count")
        .values("lesson__pk", "count")[:1]
    )

    if students_count.count() == 0:
        return False

    bestseller_id = students_count[0]["lesson__pk"]

    return lesson.id == bestseller_id


class TechnologyListSerializer(ModelSerializer):
    courses_count = SerializerMethodField("get_courses_count")

    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )

    def get_courses_count(self, technology):
        return Course.objects.filter(technology=technology).count()


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
    previous_price = SerializerMethodField("get_lesson_previous_price")
    lowest_30_days_price = SerializerMethodField("get_lesson_lowest_30_days_price")
    lecturers = SerializerMethodField("get_lesson_lecturers")
    students_count = SerializerMethodField("get_lesson_students_count")
    rating = SerializerMethodField("get_lesson_rating")
    rating_count = SerializerMethodField("get_lesson_rating_count")
    is_bestseller = SerializerMethodField("get_lesson_is_bestseller")

    def get_lesson_is_bestseller(self, lesson):
        return get_is_bestseller(lesson)

    def get_lesson_previous_price(self, lesson):
        return get_previous_price(
            price_history_model=LessonPriceHistory, instance=lesson
        )

    def get_lesson_lowest_30_days_price(self, lesson):
        return get_lowest_30_days_price(
            price_history_model=LessonPriceHistory, instance=lesson
        )

    def get_lesson_lecturers(self, lesson):
        return get_lecturers(lessons=[lesson])

    def get_lesson_rating(self, lesson):
        return get_rating(lessons=[lesson])

    def get_lesson_rating_count(self, lesson):
        return get_rating_count(lessons=[lesson])

    def get_lesson_students_count(self, lesson):
        return get_students_count(lessons=[lesson])

    class Meta:
        model = Lesson
        exclude = ("course",)


class LessonSerializer(ModelSerializer):
    id = IntegerField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "duration",
        )


class CourseListSerializer(ModelSerializer):
    technology = TechnologySerializer()
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    duration = SerializerMethodField("get_course_duration")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_course_previous_price(self, course):
        return get_previous_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_lowest_30_days_price(self, course):
        return get_lowest_30_days_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers(lessons=lessons)

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
            "github_url",
        )


class CourseGetSerializer(ModelSerializer):
    level = CharField(source="get_level_display")
    duration = SerializerMethodField("get_course_duration")
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    lessons = SerializerMethodField("get_lessons")
    technology = TechnologySerializer()
    skills = SkillSerializer(many=True)
    topics = TopicSerializer(many=True)
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    def get_lessons(self, course):
        return LessonSerializer(get_course_lessons(course=course), many=True).data

    def get_course_previous_price(self, course):
        return get_previous_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_lowest_30_days_price(self, course):
        return get_lowest_30_days_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers_details(lessons=lessons)

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
    duration = SerializerMethodField("get_course_duration")
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    lessons = LessonDetailsSerializer(many=True)
    technology = TechnologySerializer()
    skills = SkillSerializer(many=True)
    topics = TopicSerializer(many=True)
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    video = VideoBase64File(required=False)

    def get_course_previous_price(self, course):
        return get_previous_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_lowest_30_days_price(self, course):
        return get_lowest_30_days_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers(lessons=lessons)

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

        for lesson in lessons:
            duration = lesson["duration"]
            if duration % MIN_LESSON_DURATION_MINS != 0:
                raise ValidationError(
                    {
                        "lessons": f"Czas lekcji musi być wielokrotnością {MIN_LESSON_DURATION_MINS} minut."
                    }
                )

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

    def validate_lessons_github_url(self, course, lessons):
        course_github_url = course.github_url
        for lesson in lessons:
            github_url = lesson["github_url"]
            if course_github_url not in github_url:
                raise ValidationError(
                    {"lessons": f"Github url musi być podfolderem kursu."}
                )

    def add_technology(self, technology):
        obj, created = Technology.objects.get_or_create(name=technology["name"])

        return obj

    def add_skills(self, course, skills):
        objs = []
        for skill in skills:
            obj, created = Skill.objects.get_or_create(name=skill["name"])
            objs.append(obj)

        course.skills.add(*objs)

        return course

    def add_topics(self, course, topics):
        objs = []
        for topic in topics:
            obj, created = Topic.objects.get_or_create(name=topic["name"])
            objs.append(obj)

        course.topics.add(*objs)

        return course

    @staticmethod
    def is_lesson_in_list(lesson, lessons_list):
        for lesson_obj in lessons_list:
            if lesson_obj["id"] == lesson.id:
                return True

        return False

    def create_lessons(self, course, lessons):
        Lesson.objects.bulk_create(
            Lesson(
                course=course,
                title=lesson["title"],
                description=lesson["description"],
                duration=lesson["duration"],
                github_url=lesson["github_url"],
                price=lesson["price"],
                active=lesson["active"],
            )
            for lesson in lessons
        )

    def edit_lessons(self, lessons):
        for lesson in lessons:
            id = lesson.pop("id")
            obj = Lesson.objects.get(pk=id)
            obj.title = lesson.get("title", obj.title)
            obj.description = lesson.get("description", obj.description)
            obj.duration = lesson.get("duration", obj.duration)
            obj.github_url = lesson.get("github_url", obj.github_url)

            current_price = obj.price
            new_price = lesson.get("price", obj.price)

            if current_price != new_price:
                LessonPriceHistory.objects.create(lesson=obj, price=current_price)

            obj.price = new_price
            obj.active = lesson.get("active", obj.active)

            obj.save()

    def deactivate_lessons(self, lesson_ids):
        Lesson.objects.filter(id__in=lesson_ids).update(active=False)

    def manage_lessons(self, course, lessons):
        current_lessons = Lesson.objects.filter(course=course).all()
        new_lessons = [lesson for lesson in lessons if lesson["id"] == -1]
        edit_lessons = [lesson for lesson in lessons if lesson["id"] != -1]
        inactive_lessons_ids = [
            lesson.id
            for lesson in current_lessons
            if not self.is_lesson_in_list(lesson, lessons)
        ]
        self.create_lessons(course=course, lessons=new_lessons)
        self.deactivate_lessons(lesson_ids=inactive_lessons_ids)
        self.edit_lessons(lessons=edit_lessons)

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        technology = validated_data.pop("technology")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        course = Course.objects.create(
            **validated_data, technology=self.add_technology(technology=technology)
        )
        self.validate_lessons_github_url(course=course, lessons=lessons)
        self.create_lessons(course=course, lessons=lessons)
        course = self.add_skills(course=course, skills=skills)
        course = self.add_topics(course=course, topics=topics)
        course.save()

        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons")
        technology = validated_data.pop("technology")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        self.validate_lessons_github_url(course=instance, lessons=lessons)
        self.manage_lessons(course=instance, lessons=lessons)

        instance.active = validated_data.get("active", instance.active)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.level = validated_data.get("level", instance.level)

        current_price = instance.price
        new_price = validated_data.get("price", instance.price)

        if current_price != new_price:
            CoursePriceHistory.objects.create(course=instance, price=current_price)

        instance.price = new_price
        instance.github_url = validated_data.get("github_url", instance.github_url)
        instance.technology = self.add_technology(technology=technology)
        instance.skills.clear()
        instance = self.add_skills(course=instance, skills=skills)
        instance.topics.clear()
        instance = self.add_topics(course=instance, topics=topics)

        instance.save()

        return instance


class BestCourseSerializer(ModelSerializer):
    technology = TechnologySerializer()
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    duration = SerializerMethodField("get_course_duration")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")
    image = Base64ImageField(required=True)
    level = CharField(source="get_level_display")

    def get_course_previous_price(self, course):
        return get_previous_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_lowest_30_days_price(self, course):
        return get_lowest_30_days_price(
            price_history_model=CoursePriceHistory, instance=course
        )

    def get_course_duration(self, course):
        return get_duration(course)

    def get_course_lecturers(self, course):
        lessons = get_course_lessons(course=course)
        return get_lecturers(lessons=lessons)

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
            "github_url",
            "description",
        )


class CoursePriceHistorySerializer(ModelSerializer):
    class Meta:
        model = CoursePriceHistory
        fields = "__all__"


class LessonPriceHistorySerializer(ModelSerializer):
    class Meta:
        model = LessonPriceHistory
        fields = "__all__"
