from django.db import migrations
from django.contrib.auth import get_user_model
from django.conf import settings
from profile.models import Profile, LecturerProfile


def generate_dummy_lecturer(apps, schema_editor):
    email = settings.DUMMY_LECTURER_EMAIL
    password = settings.DUMMY_LECTURER_PASSWORD

    user = get_user_model()

    if not user.objects.filter(email=email).exists():
        lecturer = user.objects.create(username=email, email=email)
        lecturer.set_password(password)
        lecturer.save()

        profile = Profile.objects.create(user=lecturer, user_type="W")
        LecturerProfile.objects.create(profile=profile)


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0002_create_superuser"),
    ]

    operations = [migrations.RunPython(generate_dummy_lecturer)]
