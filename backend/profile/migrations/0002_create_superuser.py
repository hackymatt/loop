from django.db import migrations
from django.contrib.auth import get_user_model
from django.conf import settings
from profile.models import Profile


def generate_superuser(apps, schema_editor):
    email = settings.ADMIN_EMAIL
    password = settings.ADMIN_PASSWORD

    user = get_user_model()

    if not user.objects.filter(email=email).exists():
        admin = user.objects.create_superuser(
            username=email, email=email
        )
        admin.set_password(password)
        admin.save()

        Profile.objects.create(user=admin, user_type="A")


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0001_initial"),
    ]

    operations = [migrations.RunPython(generate_superuser)]
