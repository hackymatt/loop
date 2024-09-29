from django.db import migrations
from django.contrib.auth import get_user_model
from profile.models import Profile, LecturerProfile
from config_global import DUMMY_LECTURER_EMAIL, DUMMY_LECTURER_PASSWORD


def generate_dummy_lecturer(apps, schema_editor):
    user = get_user_model()

    if not user.objects.filter(email=DUMMY_LECTURER_EMAIL).exists():
        lecturer = user.objects.create(
            username=DUMMY_LECTURER_EMAIL, email=DUMMY_LECTURER_EMAIL
        )
        lecturer.set_password(DUMMY_LECTURER_PASSWORD)
        lecturer.save()

        profile = Profile.objects.create(user=lecturer, user_type="W")
        LecturerProfile.objects.create(profile=profile)


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0002_create_superuser"),
    ]

    operations = [migrations.RunPython(generate_dummy_lecturer)]
