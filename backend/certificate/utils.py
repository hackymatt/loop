from reservation.models import Reservation
from schedule.models import Schedule
from module.models import Module
from course.models import Course
from certificate.models import Certificate
from django.db.models import F
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from mailer.mailer import Mailer


def get_progress(lessons, student_profile):
    student_lessons = Reservation.objects.filter(
        student=student_profile,
        lesson__in=lessons,
        schedule__start_time__lte=make_aware(datetime.now()),
    )
    return student_lessons.count() / len(lessons)


def add_certificate(entity_type, entity, schedule, student):
    return Certificate.objects.create(
        type=entity_type,
        entity_id=entity.id,
        title=entity.title,
        duration=entity.duration,
        completed_at=schedule.end_time,
        student=student,
    )


def generate_certificates():
    mailer = Mailer()
    now = make_aware(datetime.now())

    schedules = (
        Schedule.objects.filter(lesson__isnull=False, meeting__url__isnull=False)
        .annotate(diff=now - F("end_time"))
        .filter(
            diff__lte=timedelta(minutes=30),
            diff__gt=timedelta(minutes=0),
        )
    )

    for schedule in schedules:
        reservations = Reservation.objects.filter(schedule=schedule)

        for reservation in reservations:
            certificates = []
            lesson_certificates = []
            module_certificates = []
            course_certificates = []

            student = reservation.student
            lesson = reservation.lesson

            lesson_certificates.append(lesson)
            certificates.append(f"Lekcja: {lesson}")

            modules = Module.lessons.through.objects.filter(lesson=lesson).all()
            for module in modules:
                module_lessons = module.lessons
                progress = get_progress(lessons=module_lessons, student_profile=student)
                if progress >= 1.0:
                    module_certificates.append(module)
                    certificates.append(f"Moduł: {module.title}")

            courses = Course.modules.through.objects.filter(module__in=modules).all()
            for course in courses:
                course_modules = Course.modules.through.objects.filter(
                    course=course
                ).all()
                course_lessons = Module.lessons.through.objects.filter(
                    module__in=course_modules
                ).all()
                progress = get_progress(lessons=course_lessons, student_profile=student)
                if progress >= 1.0:
                    course_certificates.append(course)
                    certificates.append(f"Kurs: {course}")

            # add certificates
            for lesson_certificate in lesson_certificates:
                add_certificate(
                    entity_type="L",
                    entity=lesson_certificate,
                    schedule=schedule,
                    student=student,
                )
            for module_certificate in module_certificates:
                add_certificate(
                    entity_type="M",
                    entity=module_certificate,
                    schedule=schedule,
                    student=student,
                )
            for course_certificate in course_certificates:
                add_certificate(
                    entity_type="K",
                    entity=course_certificate,
                    schedule=schedule,
                    student=student,
                )

            # send email
            certificates_count = len(certificates)
            data = {
                **{
                    "certificates_count": certificates_count,
                    "certificates": certificates,
                }
            }
            mailer.send(
                email_template="certificates.html",
                to=[reservation.student.profile.user.email],
                subject="Otrzymujesz nowe certifikaty"
                if certificates_count > 1
                else "Otrzymujesz nowy certifikat",
                data=data,
            )
