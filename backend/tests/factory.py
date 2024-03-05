from django.contrib.auth.models import User
from profile.models import Profile
from course.models import Course
from lesson.models import Lesson, LessonPriceHistory
from technology.models import Technology
from topic.models import Topic
from finance.models import Finance
from skill.models import Skill
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
from typing import List, Dict


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
        is_superuser=is_staff,
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
    gender: str = "M",
    phone_number: str = "123456789",
    dob: str = "1999-12-31",
    street_address: str = "Street",
    zip_code: str = "ZipCode",
    city: str = "City",
    country: str = "Country",
):
    return Profile.objects.create(
        user=user,
        verification_code=verification_code,
        verification_code_created_at=verification_code_created_at,
        user_type=user_type,
        user_title=user_title,
        gender=gender,
        phone_number=phone_number,
        dob=dob,
        street_address=street_address,
        zip_code=zip_code,
        city=city,
        country=country,
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


def find_fields(values, model):
    objs = []
    for value in values:
        obj = model.objects.get(pk=value.id)
        objs.append(obj)

    return objs


def create_course(
    title: str,
    description: str,
    level: str,
    skills,
    topics,
    lessons,
    active: bool = True,
):
    course = Course.objects.create(
        title=title,
        description=description,
        level=level,
        active=active,
    )

    course.lessons.add(*lessons)
    course.skills.add(*skills)
    course.topics.add(*topics)
    course.image = create_image()
    course.video = create_video()
    course.save()

    return course


def create_course_obj(
    title: str,
    description: str,
    level: str,
    lessons: List[Dict[str, int]],
    skills,
    topics,
    image: str = None,
    video: str = None,
):
    return {
        "title": title,
        "description": description,
        "level": level,
        "lessons": lessons,
        "skills": skills,
        "topics": topics,
        "image": image,
        "video": video,
    }


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

    lesson.technologies.add(*technologies)
    lesson.save()

    return lesson


def create_lesson_obj(
    title: str,
    description: str,
    duration: int,
    github_url: str,
    price: str,
    technologies,
    id: int = -1,
):
    return {
        "id": id,
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


def create_skill(name: str):
    return Skill.objects.create(name=name)


def create_skill_obj(name: str):
    return {"name": name}


def create_topic(name: str):
    return Topic.objects.create(name=name)


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


def create_finance(
    lecturer: Profile, account: str = None, rate: float = None, commission: int = None
):
    return Finance.objects.create(
        lecturer=lecturer, account=account, rate=rate, commission=commission
    )
