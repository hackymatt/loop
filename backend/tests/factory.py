from django.contrib.auth.models import User
from profile.models import Profile
from course.models import (
    Course,
    Skill,
    Topic,
)
from lesson.models import Lesson, LessonPriceHistory, Technology
from review.models import Review
from purchase.models import Purchase
from newsletter.models import Newsletter
from schedule.models import Schedule
from wishlist.models import Wishlist
from cart.models import Cart
from teaching.models import Teaching
from reservation.models import Reservation
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.files.uploadedfile import SimpleUploadedFile
import os


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    is_active: bool,
    is_staff: bool = False,
):
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=email,
        is_active=is_active,
        is_staff=is_staff,
    )

    user.set_password(password)
    user.save()

    return user


def create_profile(
    user: User,
    verification_code: str = "abcdefgh",
    verification_code_created_at: datetime = make_aware(datetime.now()),
    user_type: str = "S",
    user_title: str = "",
):
    return Profile.objects.create(
        user=user,
        verification_code=verification_code,
        verification_code_created_at=verification_code_created_at,
        user_type=user_type,
        user_title=user_title,
    )


def _create_file(file_name: str):
    file_path = os.path.join(os.path.dirname(__file__), "helper_files/" + file_name)
    with open(file_path, "rb") as file:
        upload_file = SimpleUploadedFile(file_name, file.read())
    return upload_file


def create_image():
    return _create_file("example_image.jpg")


def create_video():
    return _create_file("example_video.mp4")


def create_field(value, model):
    obj, _ = model.objects.get_or_create(name=value["name"])

    return obj


def create_fields(values, model):
    objs = []
    for value in values:
        obj, _ = model.objects.get_or_create(name=value["name"])
        objs.append(obj)

    return objs


def create_course(
    title: str,
    description: str,
    technology,
    level: str,
    price: str,
    github_url: str,
    skills,
    topics,
    lessons,
    active: bool = True,
):
    course = Course.objects.create(
        title=title,
        description=description,
        level=level,
        price=price,
        github_url=github_url,
        active=active,
    )

    course.technology.add(*create_fields(technology, Technology))
    course.skills.add(*create_fields(skills, Skill))
    course.topics.add(*create_fields(topics, Topic))
    course.image = create_image()
    course.video = create_video()
    course.save()

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

    return course


def create_lesson(
    title: str,
    description: str,
    duration: int,
    github_url: str,
    price: str,
    technologies,
):
    lesson = Lesson.objects.create(
        title=title,
        description=description,
        duration=duration,
        github_url=github_url,
        price=price,
    )

    lesson.technologies.add(*create_fields(technologies, Technology))
    lesson.save()

    return lesson


def create_lesson_obj(
    title: str,
    description: str,
    duration: int,
    github_url: str,
    price: str,
    technologies,
):
    return {
        "title": title,
        "description": description,
        "duration": duration,
        "github_url": github_url,
        "price": price,
        "technologies": technologies,
    }


def create_technology(name: str):
    return Technology.objects.create(name=name)


def create_technology_obj(name: str):
    return {"name": name}


def create_skill_obj(name: str):
    return {"name": name}


def create_topic_obj(name: str):
    return {"name": name}


def create_review(
    lesson: Lesson, student: Profile, lecturer: Profile, rating: int, review: str = None
):
    return Review.objects.create(
        lesson=lesson, student=student, lecturer=lecturer, rating=rating, review=review
    )


def create_purchase(
    lesson: Lesson,
    student: Profile,
    price: float,
):
    return Purchase.objects.create(
        lesson=lesson,
        student=student,
        price=price,
    )


def create_newsletter(email: str, active: bool = True):
    return Newsletter.objects.create(email=email, active=active)


def create_schedule(
    lecturer: Profile,
    time: str,
):
    return Schedule.objects.create(lecturer=lecturer, time=time)


def create_course_price_history(course: Course, price: float):
    return CoursePriceHistory.objects.create(course=course, price=price)


def create_lesson_price_history(lesson: Lesson, price: float):
    return LessonPriceHistory.objects.create(lesson=lesson, price=price)


def create_wishlist(student: Profile, lesson: Lesson):
    return Wishlist.objects.create(student=student, lesson=lesson)


def create_cart(student: Profile, lesson: Lesson):
    return Cart.objects.create(student=student, lesson=lesson)


def create_teaching(lecturer: Profile, lesson: Lesson):
    return Teaching.objects.create(lecturer=lecturer, lesson=lesson)


def create_reservation(student: Profile, lesson: Lesson, schedule: Schedule):
    return Reservation.objects.create(student=student, lesson=lesson, schedule=schedule)
