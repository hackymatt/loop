from message.models import Message
from datetime import datetime, timedelta

MESSAGE_EXPIRY_DAYS = 31


def remove_old_messages():
    messages = Message.objects.filter(
        created_at__lt=datetime.now() - timedelta(days=MESSAGE_EXPIRY_DAYS)
    ).exclude(status="NEW")
    messages.delete()
