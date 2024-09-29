from reservation.models import Reservation
from schedule.models import Schedule
from module.models import Module
from course.models import Course
from lesson.models import Lesson
from certificate.models import Certificate
from profile.models import StudentProfile
from django.db.models import F, Sum
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from mailer.mailer import Mailer
from notification.utils import notify
from config_global import FRONTEND_URL


def get_progress(lessons, student_profile):
    student_lessons = Reservation.objects.filter(
        student=student_profile,
        lesson__in=lessons,
        schedule__end_time__lte=make_aware(datetime.now()),
    )
    return student_lessons.count() / len(lessons)


def get_duration(modules):
    lessons_ids = (
        Module.lessons.through.objects.filter(module__in=modules)
        .distinct()
        .values("lesson_id")
    )
    lessons = Lesson.objects.filter(id__in=lessons_ids).all()
    return lessons.aggregate(Sum("duration"))["duration__sum"]


def add_certificate(entity_type, entity, student):
    if entity_type == "L":
        duration = entity.duration
    elif entity_type == "M":
        duration = get_duration(modules=[entity])
    else:
        course_modules = (
            Course.modules.through.objects.filter(course=entity)
            .distinct()
            .values("module_id")
            .order_by("id")
        )
        duration = get_duration(modules=course_modules)

    return Certificate.objects.get_or_create(
        type=entity_type,
        entity_id=entity.id,
        title=entity.title,
        duration=duration,
        student=student,
    )


def transform_list(input_list):
    # Mapping of old keys to new keys
    key_mapping = {"L": "Lekcje", "M": "Moduły", "K": "Kursy"}

    transformed = []

    # Create a dictionary to keep track of items by type
    temp_dict = {}

    for item in input_list:
        item_type = item["type"]
        # Use the mapping to get the new key
        new_type = key_mapping.get(item_type, item_type)

        # If the type doesn't exist in temp_dict, initialize it
        if new_type not in temp_dict:
            temp_dict[new_type] = {"type": new_type, "certificates": []}
        # Append the item to the "certificates" list
        temp_dict[new_type]["certificates"].append(item)

    # Sort each "certificates" list based on the "name" property
    for key in temp_dict:
        temp_dict[key]["certificates"].sort(key=lambda x: x["name"])

    # Convert the dictionary to a list of values
    transformed = list(temp_dict.values())

    return transformed


def generate_certificates():
    mailer = Mailer()
    now = make_aware(datetime.now())

    reservations = (
        Reservation.objects.all()
        .annotate(diff=now - F("schedule__end_time"))
        .filter(
            diff__lte=timedelta(hours=24),
            diff__gt=timedelta(hours=0),
        )
    )
    students = reservations.distinct().values("student").distinct()
    for student in students:
        certificates = []
        student_obj = StudentProfile.objects.get(pk=student["student"])
        lessons = reservations.filter(student=student_obj).distinct().values("lesson")

        for lesson in lessons:
            lesson_obj = Lesson.objects.get(pk=lesson["lesson"])
            certificate, created = add_certificate(
                entity_type="L", entity=lesson_obj, student=student_obj
            )
            if created:
                certificates.append(
                    {
                        "type": "L",
                        "name": lesson_obj.title,
                        "url": f"{FRONTEND_URL}/certificate/{certificate.uuid}",
                    }
                )

            modules = (
                Module.lessons.through.objects.filter(lesson=lesson_obj)
                .distinct()
                .values("module_id")
            )
            for module in modules:
                module_obj = Module.objects.get(pk=module["module_id"])
                module_lessons = module_obj.lessons.all()
                progress = get_progress(
                    lessons=module_lessons, student_profile=student_obj
                )
                if progress >= 1.0:
                    certificate, created = add_certificate(
                        entity_type="M", entity=module_obj, student=student_obj
                    )
                    if created:
                        certificates.append(
                            {
                                "type": "M",
                                "name": module_obj.title,
                                "url": f"{FRONTEND_URL}/certificate/{certificate.uuid}",
                            }
                        )

            courses = (
                Course.modules.through.objects.filter(module__in=modules)
                .distinct()
                .values("course_id")
            )
            for course in courses:
                course_obj = Course.objects.get(pk=course["course_id"])
                course_modules = (
                    Course.modules.through.objects.filter(course=course_obj)
                    .distinct()
                    .values("module_id")
                )
                course_lessons = (
                    Module.lessons.through.objects.filter(module__in=course_modules)
                    .distinct()
                    .values("lesson_id")
                )
                progress = get_progress(
                    lessons=course_lessons, student_profile=student_obj
                )
                if progress >= 1.0:
                    certificate, created = add_certificate(
                        entity_type="K", entity=course_obj, student=student_obj
                    )
                    if created:
                        certificates.append(
                            {
                                "type": "K",
                                "name": course_obj.title,
                                "url": f"{FRONTEND_URL}/certificate/{certificate.uuid}",
                            }
                        )

        # send email
        certificates_count = len(certificates)
        if certificates_count > 0:
            data = {
                **{
                    "certificates_count": certificates_count,
                    "types_certificates": transform_list(certificates),
                }
            }
            mailer.send(
                email_template="new_certificates.html",
                to=[student_obj.profile.user.email],
                subject="Gratulacje! Otrzymujesz nowe certyfikaty",
                data=data,
            )
            certificate_str = ", ".join(
                [certificate["name"] for certificate in certificates]
            )
            notify(
                profile=student_obj.profile,
                title="Gratulacje! Otrzymujesz nowe certyfikaty",
                subtitle=f"Liczba certyfikatów: {certificates_count}",
                description=f"Poniżej znajduje się lista nowo otrzymanych certyfikatów: {certificate_str}.",
                path=f"/account/certificates?sort_by=-completed_at&page_size=10&completed_at={datetime.now().strftime('%Y-%m-%d')}",
                icon="mdi:certificate",
            )
