from django.core.management import call_command


def create_backup():
    try:
        call_command("dbbackup")
        call_command("mediabackup")
    except Exception:
        pass
