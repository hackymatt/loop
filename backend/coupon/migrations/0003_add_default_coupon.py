from django.db import migrations
from config_global import DEFAULT_COUPON


def add_coupon(apps, schema_editor):
    Coupon = apps.get_model("coupon", "Coupon")
    Coupon.objects.get_or_create(**DEFAULT_COUPON)


class Migration(migrations.Migration):
    dependencies = [
        ("coupon", "0002_alter_couponuser_coupon_alter_couponuser_user"),
    ]

    operations = [migrations.RunPython(add_coupon)]
