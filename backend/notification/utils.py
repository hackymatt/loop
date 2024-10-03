from notification.models import Notification
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from config_global import NOTIFICATION_EXPIRY_DAYS


def remove_old_notifications():
    date = make_aware(datetime.now() - timedelta(days=NOTIFICATION_EXPIRY_DAYS))
    notifications = Notification.objects.filter(created_at__lt=date).exclude(
        status="NEW"
    )
    notifications.delete()


def notify(
    profile,
    title: str,
    subtitle: str,
    description: str,
    path: str,
    icon: str,
):
    return Notification.objects.get_or_create(
        profile=profile,
        title=title,
        subtitle=subtitle,
        description=description,
        path=path,
        icon=icon,
    )
