from django.contrib.auth.models import User
from profile.models import Profile
from course.models import Course, Lesson, Technology, Skill, Topic
from review.models import Review
from datetime import datetime
from django.utils.timezone import make_aware
from PIL import Image
from io import BytesIO


def create_user(
    first_name: str, last_name: str, email: str, password: str, is_active: bool
):
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=email,
        is_active=is_active,
    )

    user.set_password(password)
    user.save()

    return user


def create_profile(
    user: User,
    verification_code: str = "abcdefgh",
    verification_code_created_at: datetime = make_aware(datetime.now()),
    user_type: str = "S",
):
    return Profile.objects.create(
        user=user,
        verification_code=verification_code,
        verification_code_created_at=verification_code_created_at,
        user_type=user_type,
    )


def create_image():
    image_data = BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(image_data, format="png")
    image_data.seek(0)

    return image_data


def create_field(value, model):
    obj, created = model.objects.get_or_create(name=value["name"])

    return obj


def create_fields(values, model):
    objs = []
    for value in values:
        obj, created = model.objects.get_or_create(name=value["name"])
        objs.append(obj)

    return objs


def add_lecturers(lesson, lecturers):
    uuids = [lecturer["uuid"] for lecturer in lecturers]
    objs = Profile.objects.filter(uuid__in=uuids)

    lesson.lecturers.add(*objs)

    return lesson


def create_course(
    title: str,
    description: str,
    technology,
    level: str,
    price: str,
    github_repo_link: str,
    skills,
    topics,
    lessons,
):
    course = Course.objects.create(
        title=title,
        description=description,
        technology=create_field(technology, Technology),
        level=level,
        price=price,
        github_repo_link=github_repo_link,
    )

    course.skills.add(*create_fields(skills, Skill))
    course.topics.add(*create_fields(topics, Topic))
    course.save()

    for lesson in lessons:
        obj = Lesson.objects.create(
            course=course,
            title=lesson["title"],
            description=lesson["description"],
            duration=lesson["duration"],
            github_branch_link=lesson["github_branch_link"],
            price=lesson["price"],
        )
        obj = add_lecturers(lesson=obj, lecturers=lesson["lecturers"])
        obj.save()

    return course


def create_lesson_obj(
    id: int,
    title: str,
    description: str,
    duration: int,
    github_branch_link: str,
    price: str,
    lecturers,
):
    return {
        "id": id,
        "title": title,
        "description": description,
        "duration": duration,
        "github_branch_link": github_branch_link,
        "price": price,
        "lecturers": lecturers,
    }


def create_lecturer_obj(lecturer: Profile):
    return {
        "uuid": lecturer.uuid,
        "first_name": lecturer.user.first_name,
        "last_name": lecturer.user.last_name,
        "email": lecturer.user.email,
    }


def create_technology(name: str):
    return Technology.objects.create(name=name)


def create_technology_obj(name: str):
    return {"name": name}


def create_skill_obj(name: str):
    return {"name": name}


def create_topic_obj(name: str):
    return {"name": name}


def create_review(lesson: Lesson, profile: Profile, rating: int, review: str = None):
    return Review.objects.create(
        lesson=lesson, profile=profile, rating=rating, review=review
    )
