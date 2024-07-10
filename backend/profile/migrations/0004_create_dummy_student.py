from django.db import migrations
from django.contrib.auth import get_user_model
from django.conf import settings
from profile.models import Profile, StudentProfile


def generate_dummy_student(apps, schema_editor):
    email = settings.DUMMY_STUDENT_EMAIL
    password = settings.DUMMY_STUDENT_PASSWORD

    user = get_user_model()

    if not user.objects.filter(email=email).exists():
        student = user.objects.create(username=email, email=email)
        student.set_password(password)
        student.save()

        profile = Profile.objects.create(user=student, user_type="S")
        StudentProfile.objects.create(profile=profile)


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0003_create_dummy_lecturer"),
    ]

    operations = [migrations.RunPython(generate_dummy_student)]
