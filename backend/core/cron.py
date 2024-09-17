from django.core.management import call_command, CommandError
from reservation.utils import confirm_reservations
from review.utils import remind_review
from certificate.utils import generate_certificates
from notification.utils import remove_old_notifications
from message.utils import remove_old_messages


def create_backup():
    try:
        call_command("dbbackup")
    except CommandError:
        pass


def confirm_lessons():
    try:
        confirm_reservations()
    except Exception:
        pass


def remind_lessons_review():
    try:
        remind_review()
    except Exception:
        pass


def create_certificates():
    try:
        generate_certificates()
    except Exception:
        pass


def cleanse_notifications():
    try:
        remove_old_notifications()
    except Exception:
        pass


def cleanse_messages():
    try:
        remove_old_messages()
    except Exception:
        pass
