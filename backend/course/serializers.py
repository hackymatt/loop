from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    EmailField,
)
from rest_framework.serializers import ValidationError
from course.models import Lesson, Course, Skill, Topic
from profile.models import Profile
from django.db.models import Sum


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
        fields = ("uuid", "first_name", "last_name", "email")


class LessonSerializer(ModelSerializer):
    lecturers = LecturerSerializer(many=True)

    class Meta:
        model = Lesson
        exclude = ("course",)


class CourseListSerializer(ModelSerializer):
    duration = SerializerMethodField("get_duration")
    lecturers = SerializerMethodField("get_lecturers")

    def get_duration(self, course):
        return Lesson.objects.filter(course=course).aggregate(Sum("duration"))[
            "duration__sum"
        ]

    def get_lecturers(self, course):
        lessons = LessonSerializer(Lesson.objects.filter(course=course), many=True).data
        lecturers = [lesson["lecturers"] for lesson in lessons]
        lecturers_joined = sum(lecturers, [])
        lecturers_unique = [
            dict(y) for y in set(tuple(x.items()) for x in lecturers_joined)
        ]

        return lecturers_unique

    class Meta:
        model = Course
        exclude = ("active", "skills", "topics")


class CourseSerializer(ModelSerializer):
    duration = SerializerMethodField("get_duration")
    lessons = LessonSerializer(many=True)
    skills = SkillSerializer(many=True)
    topics = TopicSerializer(many=True)
    lecturers = SerializerMethodField("get_lecturers")

    def get_duration(self, course):
        return Lesson.objects.filter(course=course).aggregate(Sum("duration"))[
            "duration__sum"
        ]

    def get_lecturers(self, course):
        lessons = LessonSerializer(Lesson.objects.filter(course=course), many=True).data
        lecturers = [lesson["lecturers"] for lesson in lessons]
        lecturers_joined = sum(lecturers, [])
        lecturers_unique = [
            dict(y) for y in set(tuple(x.items()) for x in lecturers_joined)
        ]

        return lecturers_unique

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

    def add_lecturers(self, lesson, lecturers):
        uuids = [lecturer["uuid"] for lecturer in lecturers]
        objs = Profile.objects.filter(uuid__in=uuids)

        lesson.lecturers.add(*objs)

        return lesson

    def create_lessons(self, course, lessons):
        for lesson in lessons:
            obj = Lesson.objects.create(
                course=course,
                title=lesson["title"],
                description=lesson["description"],
                duration=lesson["duration"],
                github_branch_link=lesson["github_branch_link"],
                price=lesson["price"],
            )
            obj = self.add_lecturers(lesson=obj, lecturers=lesson["lecturers"])
            obj.save()

    def delete_lessons(self, course):
        Lesson.objects.filter(course=course).all().delete()

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        course = Course.objects.create(**validated_data)
        self.create_lessons(course=course, lessons=lessons)
        course = self.add_skills(course=course, skills=skills)
        course = self.add_topics(course=course, topics=topics)
        course.save()

        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons")
        skills = validated_data.pop("skills")
        topics = validated_data.pop("topics")

        self.delete_lessons(course=instance)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.technology = validated_data.get("technology", instance.technology)
        instance.level = validated_data.get("level", instance.level)
        instance.price = validated_data.get("price", instance.price)
        instance.github_repo_link = validated_data.get(
            "github_repo_link", instance.github_repo_link
        )
        instance.skills.clear()
        instance = self.add_skills(course=instance, skills=skills)
        instance.topics.clear()
        instance = self.add_topics(course=instance, topics=topics)

        instance.save()

        self.create_lessons(course=instance, lessons=lessons)

        return instance
