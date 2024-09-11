from notification.models import Notification
from datetime import datetime, timedelta

NOTIFICATION_EXPIRY_DAYS = 31


def remove_old_notifications():
    notifications = Notification.objects.filter(
        created_at__lt=datetime.now() - timedelta(days=NOTIFICATION_EXPIRY_DAYS)
    ).exclude(status="NEW")
    notifications.delete()


def notify(
    profile,
    title: str,
    lesson: str,
    description: str,
    path: str,
    icon: str,
):
    return Notification.objects.create(
        profile=profile,
        title=title,
        lesson=lesson,
        description=description,
        status="NEW",
        path=path,
        icon=icon,
    )
