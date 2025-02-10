from django.contrib.auth.models import User
from profile.models import (
    Profile,
    LecturerProfile,
    AdminProfile,
    StudentProfile,
    OtherProfile,
)
from course.models import Course
from coupon.models import Coupon, CouponUser
from lesson.models import Lesson, LessonPriceHistory
from technology.models import Technology
from topic.models import Topic
from candidate.models import Candidate
from finance.models import Finance, FinanceHistory
from tag.models import Tag
from review.models import Review
from module.models import Module
from purchase.models import Purchase, Payment
from newsletter.models import Newsletter
from notification.models import Notification
from message.models import Message
from schedule.models import Schedule, Meeting, Recording
from wishlist.models import Wishlist
from post.models import Post, PostCategory
from cart.models import Cart
from teaching.models import Teaching
from reservation.models import Reservation
from certificate.models import Certificate
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from typing import List, Dict
from django.db.models import Sum


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


def create_admin_profile(profile: Profile):
    return AdminProfile.objects.create(
        profile=profile,
    )


def create_student_profile(profile: Profile):
    return StudentProfile.objects.create(
        profile=profile,
    )


def create_lecturer_profile(
    profile: Profile, title: str = "", description: str = "", linkedin_url: str = ""
):
    return LecturerProfile.objects.create(
        profile=profile,
        title=title,
        description=description,
        linkedin_url=linkedin_url,
    )


def create_other_profile(profile: Profile):
    return OtherProfile.objects.create(
        profile=profile,
    )


def create_profile(
    user: User,
    verification_code: str = "abcdefgh",
    verification_code_created_at: datetime = make_aware(datetime.now()),
    user_type: str = "S",
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
    overview: str,
    level: str,
    tags,
    topics,
    candidates,
    modules,
    active: bool = True,
):
    course = Course.objects.create(
        title=title,
        description=description,
        overview=overview,
        level=level,
        active=active,
    )

    course.modules.add(*modules)
    course.tags.add(*tags)
    course.topics.add(*topics)
    course.candidates.add(*candidates)
    course.image = create_image()
    course.video = create_video()
    course.save()

    return course


def create_course_obj(
    title: str,
    description: str,
    overview: str,
    level: str,
    modules: List[Dict[str, int]],
    tags,
    topics,
    candidates,
    image: str = None,
    video: str = None,
    active: bool = True,
):
    return {
        "title": title,
        "description": description,
        "overview": overview,
        "level": level,
        "modules": modules,
        "tags": tags,
        "topics": topics,
        "candidates": candidates,
        "image": image,
        "video": video,
        "active": active,
    }


def create_module(
    title: str,
    lessons,
):
    module = Module.objects.create(
        title=title,
    )

    module.lessons.add(*lessons)
    module.save()

    return module


def create_module_obj(
    title: str,
    lessons,
    id: int = -1,
):
    return {
        "id": id,
        "title": title,
        "lessons": lessons,
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
    active: bool = True,
):
    return {
        "id": id,
        "title": title,
        "description": description,
        "duration": duration,
        "github_url": github_url,
        "price": price,
        "technologies": technologies,
        "active": active,
    }


def create_technology(name: str, description: str = "description"):
    return Technology.objects.create(name=name, description=description)


def create_technology_obj(name: str, description: str = "description"):
    return {"name": name, "description": description}


def create_tag(name: str):
    return Tag.objects.create(name=name)


def create_tag_obj(name: str):
    return {"name": name}


def create_topic(name: str):
    return Topic.objects.create(name=name)


def create_candidate(name: str):
    return Candidate.objects.create(name=name)


def create_topic_obj(name: str):
    return {"name": name}


def create_candidate_obj(name: str):
    return {"name": name}


def create_review(
    lesson: Lesson,
    student: Profile,
    lecturer: LecturerProfile,
    rating: int,
    review: str = None,
):
    return Review.objects.create(
        lesson=lesson, student=student, lecturer=lecturer, rating=rating, review=review
    )


def create_payment(amount: int, status: str = "S"):
    return Payment.objects.create(amount=float(amount) * 100, status=status)


def create_payment_obj(amount: int, status: str = "Success"):
    return {"amount": amount, "status": status}


def create_purchase(
    lesson: Lesson,
    student: Profile,
    price: float,
    payment: Payment,
):
    return Purchase.objects.create(
        lesson=lesson,
        student=student,
        price=price,
        payment=payment,
    )


def create_newsletter(email: str, active: bool = True):
    return Newsletter.objects.create(email=email, active=active)


def create_schedule(
    lecturer: LecturerProfile, start_time: str, end_time: str, lesson: Lesson = None
):
    return Schedule.objects.create(
        lecturer=lecturer, start_time=start_time, end_time=end_time, lesson=lesson
    )


def create_schedule_obj(start_time: str, end_time: str):
    return {"start_time": start_time, "end_time": end_time}


def create_lesson_price_history(lesson: Lesson, price: float):
    return LessonPriceHistory.objects.create(lesson=lesson, price=price)


def create_wishlist(student: Profile, lesson: Lesson):
    return Wishlist.objects.create(student=student, lesson=lesson)


def create_cart(student: Profile, lesson: Lesson):
    return Cart.objects.create(student=student, lesson=lesson)


def create_teaching(lecturer: LecturerProfile, lesson: Lesson):
    return Teaching.objects.create(lecturer=lecturer, lesson=lesson)


def create_reservation(
    student: Profile, lesson: Lesson, schedule: Schedule, purchase: Purchase
):
    return Reservation.objects.create(
        student=student, lesson=lesson, schedule=schedule, purchase=purchase
    )


def create_finance(
    lecturer: LecturerProfile,
    account: str = None,
    rate: float = None,
    commission: int = None,
):
    return Finance.objects.create(
        lecturer=lecturer, account=account, rate=rate, commission=commission
    )


def create_finance_history(
    lecturer: LecturerProfile,
    account: str = None,
    rate: float = None,
    commission: int = None,
):
    return FinanceHistory.objects.create(
        lecturer=lecturer, account=account, rate=rate, commission=commission
    )


def create_coupon(
    code: str,
    discount: float,
    is_percentage: bool,
    all_users: bool,
    is_infinite: bool,
    active: bool,
    expiration_date: datetime,
    users: List[int] = [],
    max_uses: int = 1,
    uses_per_user: int = 1,
    min_total: int = 100,
):
    coupon = Coupon.objects.create(
        code=code,
        discount=discount,
        is_percentage=is_percentage,
        all_users=all_users,
        is_infinite=is_infinite,
        max_uses=max_uses,
        uses_per_user=uses_per_user,
        active=active,
        expiration_date=expiration_date,
        min_total=min_total,
    )

    coupon.users.add(*users)

    return coupon


def create_coupon_obj(
    code: str,
    discount: float,
    is_percentage: bool,
    all_users: bool,
    users: List[int],
    is_infinite: bool,
    max_uses: int,
    uses_per_user: int,
    active: bool,
    expiration_date,
    min_total: float,
):
    return {
        "code": code,
        "discount": discount,
        "is_percentage": is_percentage,
        "all_users": all_users,
        "users": users,
        "is_infinite": is_infinite,
        "max_uses": max_uses,
        "uses_per_user": uses_per_user,
        "active": active,
        "expiration_date": expiration_date,
        "min_total": min_total,
    }


def create_coupon_user(coupon: Coupon, user: Profile, payment: Payment):
    return CouponUser.objects.create(coupon=coupon, user=user, payment=payment)


def create_meeting(event_id: str, url: str):
    return Meeting.objects.create(event_id=event_id, url=url)


def create_certificate(entity_type, entity, student):
    if entity_type == "L":
        duration = entity.duration
    elif entity_type == "M":
        lessons_ids = entity.lessons.through.objects.filter(module=entity).values(
            "lesson_id"
        )
        lessons = Lesson.objects.filter(id__in=lessons_ids).all()
        duration = lessons.aggregate(Sum("duration"))["duration__sum"]
    else:
        course_modules = (
            Course.modules.through.objects.filter(course=entity)
            .values("module_id")
            .order_by("id")
        )
        lessons_ids = Module.lessons.through.objects.filter(
            module__in=course_modules
        ).values("lesson_id")
        lessons = Lesson.objects.filter(id__in=lessons_ids).all()
        duration = lessons.aggregate(Sum("duration"))["duration__sum"]

    return Certificate.objects.create(
        type=entity_type,
        entity_id=entity.id,
        title=entity.title,
        duration=duration,
        student=student,
    )


def create_notification(
    profile: Profile,
    title: str,
    subtitle: str,
    description: str,
    status: str,
    path: str,
    icon: str,
):
    return Notification.objects.create(
        profile=profile,
        title=title,
        subtitle=subtitle,
        description=description,
        status=status,
        path=path,
        icon=icon,
    )


def create_message(
    sender: Profile,
    recipient: Profile,
    subject: str,
    body: str,
    status: str,
):
    return Message.objects.create(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        status=status,
    )


def create_post_category(name: str):
    return PostCategory.objects.create(name=name)


def create_post_category_obj(name: str):
    return {"name": name}


def create_post(
    title: str,
    description: str,
    content: str,
    category: PostCategory,
    authors,
    tags,
    publication_date: datetime,
    active: bool = True,
):
    post = Post.objects.create(
        title=title,
        description=description,
        content=content,
        category=category,
        publication_date=publication_date,
        active=active,
    )

    post.authors.add(*authors)
    post.tags.add(*tags)
    post.image = create_image()
    post.save()

    return post


def create_post_obj(
    title: str,
    description: str,
    content: str,
    category: str,
    authors,
    tags,
    publication_date,
    image: str = None,
    active: bool = True,
):
    return {
        "title": title,
        "description": description,
        "content": content,
        "category": category,
        "authors": authors,
        "tags": tags,
        "image": image,
        "publication_date": publication_date,
        "active": active,
    }


def create_recording(
    schedule: Schedule,
    file_id: str = "00001",
    file_name: str = "file_123",
    file_url: str = "https://example.com/file.mp4",
):
    return Recording.objects.create(
        schedule=schedule, file_id=file_id, file_name=file_name, file_url=file_url
    )
