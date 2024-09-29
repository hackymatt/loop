from django.db import migrations
from django.contrib.auth import get_user_model
from profile.models import Profile, AdminProfile
from config_global import ADMIN_EMAIL, ADMIN_PASSWORD


def generate_superuser(apps, schema_editor):
    user = get_user_model()

    if not user.objects.filter(email=ADMIN_EMAIL).exists():
        admin = user.objects.create_superuser(username=ADMIN_EMAIL, email=ADMIN_EMAIL)
        admin.set_password(ADMIN_PASSWORD)
        admin.save()

        profile = Profile.objects.create(user=admin, user_type="A")
        AdminProfile.objects.create(profile=profile)


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0001_initial"),
    ]

    operations = [migrations.RunPython(generate_superuser)]
