from django.core.management import call_command, CommandError
from reservation.utils import confirm_reservations
from review.utils import remind_review


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
