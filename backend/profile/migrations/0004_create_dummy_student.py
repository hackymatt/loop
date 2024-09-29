from django.db import migrations
from django.contrib.auth import get_user_model
from profile.models import Profile, StudentProfile
from config_global import DUMMY_STUDENT_EMAIL, DUMMY_STUDENT_PASSWORD


def generate_dummy_student(apps, schema_editor):
    user = get_user_model()

    if not user.objects.filter(email=DUMMY_STUDENT_EMAIL).exists():
        student = user.objects.create(
            username=DUMMY_STUDENT_EMAIL, email=DUMMY_STUDENT_EMAIL
        )
        student.set_password(DUMMY_STUDENT_PASSWORD)
        student.save()

        profile = Profile.objects.create(user=student, user_type="S")
        StudentProfile.objects.create(profile=profile)


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0003_create_dummy_lecturer"),
    ]

    operations = [migrations.RunPython(generate_dummy_student)]
