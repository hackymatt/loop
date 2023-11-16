from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    EmailField,
    IntegerField,
)
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
from purchase.models import Purchase
from schedule.models import Schedule
from django.db.models import Sum, Avg, Min
from django.core.exceptions import FieldDoesNotExist
from datetime import timedelta


def model_field_exists(obj, field):
    try:
        obj._meta.get_field(field)
        return True
    except (AttributeError, FieldDoesNotExist):
        return False


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
    lecturer_ids = Schedule.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = Profile.objects.filter(id__in=lecturer_ids).order_by("uuid")
    return LecturerSerializer(lecturers, many=True).data


def get_rating(lessons):
    return Review.objects.filter(lesson__in=lessons).aggregate(Avg("rating"))[
        "rating__avg"
    ]


def get_rating_count(lessons):
    return Review.objects.filter(lesson__in=lessons).count()


def get_students_count(lessons):
    return Purchase.objects.filter(lesson__in=lessons).count()


def get_duration(course):
    return Lesson.objects.filter(course=course).aggregate(Sum("duration"))[
        "duration__sum"
    ]


class TechnologyListSerializer(ModelSerializer):
    courses_count = SerializerMethodField("get_courses_count")

    class Meta:
        model = Technology
        fields = "__all__"

    def get_courses_count(self, technology):
        return Course.objects.filter(technology=technology).count()


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class LecturerSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "first_name",
            "last_name",
            "email",
            "image",
        )


class LessonSerializer(ModelSerializer):
    id = IntegerField()
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


class CourseListSerializer(ModelSerializer):
    technology = TechnologySerializer()
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    duration = SerializerMethodField("get_course_duration")
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")

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
        lessons = Lesson.objects.filter(course=course)
        return get_lecturers(lessons=lessons)

    def get_course_rating(self, course):
        lessons = course.lessons.all()
        return get_rating(lessons=lessons)

    def get_course_rating_count(self, course):
        lessons = course.lessons.all()
        return get_rating_count(lessons=lessons)

    def get_course_students_count(self, course):
        lessons = course.lessons.all()
        return get_students_count(lessons=lessons)

    class Meta:
        model = Course
        exclude = ("active", "skills", "topics")


class CourseSerializer(ModelSerializer):
    duration = SerializerMethodField("get_course_duration")
    previous_price = SerializerMethodField("get_course_previous_price")
    lowest_30_days_price = SerializerMethodField("get_course_lowest_30_days_price")
    lessons = LessonSerializer(many=True)
    technology = TechnologySerializer()
    skills = SkillSerializer(many=True)
    topics = TopicSerializer(many=True)
    lecturers = SerializerMethodField("get_course_lecturers")
    students_count = SerializerMethodField("get_course_students_count")
    rating = SerializerMethodField("get_course_rating")
    rating_count = SerializerMethodField("get_course_rating_count")

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
        lessons = Lesson.objects.filter(course=course)
        return get_lecturers(lessons=lessons)

    def get_course_rating(self, course):
        lessons = course.lessons.all()
        return get_rating(lessons=lessons)

    def get_course_rating_count(self, course):
        lessons = course.lessons.all()
        return get_rating_count(lessons=lessons)

    def get_course_students_count(self, course):
        lessons = course.lessons.all()
        return get_students_count(lessons=lessons)

    class Meta:
        model = Course
        exclude = ("active",)

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
                github_branch_link=lesson["github_branch_link"],
                price=lesson["price"],
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
            obj.github_branch_link = lesson.get(
                "github_branch_link", obj.github_branch_link
            )

            current_price = obj.price
            new_price = lesson.get("price", obj.price)

            if current_price != new_price:
                LessonPriceHistory.objects.create(lesson=obj, price=current_price)

            obj.price = new_price

            obj.save()

    def delete_lessons(self, lesson_ids):
        Lesson.objects.filter(id__in=lesson_ids).delete()

    def manage_lessons(self, course, lessons):
        current_lessons = Lesson.objects.filter(course=course).all()
        new_lessons = [lesson for lesson in lessons if lesson["id"] == -1]
        edit_lessons = [lesson for lesson in lessons if lesson["id"] != -1]
        delete_lessons = [
            lesson.id
            for lesson in current_lessons
            if not self.is_lesson_in_list(lesson, lessons)
        ]
        self.create_lessons(course=course, lessons=new_lessons)
        self.delete_lessons(lesson_ids=delete_lessons)
        self.edit_lessons(lessons=edit_lessons)

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        technology = validated_data.pop("technology")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        course = Course.objects.create(
            **validated_data, technology=self.add_technology(technology=technology)
        )
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

        self.manage_lessons(course=instance, lessons=lessons)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.level = validated_data.get("level", instance.level)

        current_price = instance.price
        new_price = validated_data.get("price", instance.price)

        if current_price != new_price:
            CoursePriceHistory.objects.create(course=instance, price=current_price)

        instance.price = new_price
        instance.github_repo_link = validated_data.get(
            "github_repo_link", instance.github_repo_link
        )
        instance.technology = self.add_technology(technology=technology)
        instance.skills.clear()
        instance = self.add_skills(course=instance, skills=skills)
        instance.topics.clear()
        instance = self.add_topics(course=instance, topics=topics)

        instance.save()

        return instance
