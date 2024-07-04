from django.core.management import call_command, CommandError
from reservation.utils import confirm_reservations


def create_backup():
    try:
        call_command("dbbackup")
        call_command("mediabackup")
    except CommandError:
        pass


def confirm_lessons():
    confirm_reservations()
