from message.models import Message
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from config_global import MESSAGE_EXPIRY_DAYS
from const import StatusType


def remove_old_messages():
    date = make_aware(datetime.now() - timedelta(days=MESSAGE_EXPIRY_DAYS))
    messages = Message.objects.filter(created_at__lt=date).exclude(
        status=StatusType.NEW
    )
    messages.delete()
