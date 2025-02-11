from django.db import migrations
from django.contrib.auth import get_user_model
from profile.models import Profile, OtherProfile
from config_global import DUMMY_OTHER_EMAIL, DUMMY_OTHER_PASSWORD


def generate_dummy_other(apps, schema_editor):
    user = get_user_model()

    if not user.objects.filter(email=DUMMY_OTHER_EMAIL).exists():
        student = user.objects.create(
            username=DUMMY_OTHER_EMAIL, email=DUMMY_OTHER_EMAIL
        )
        student.set_password(DUMMY_OTHER_PASSWORD)
        student.save()

        profile = Profile.objects.create(user=student, user_type="I")
        OtherProfile.objects.create(profile=profile)


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0005_alter_profile_user_type_otherprofile"),
    ]

    operations = [migrations.RunPython(generate_dummy_other)]
