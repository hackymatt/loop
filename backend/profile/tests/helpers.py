from django.contrib.auth.models import User
from profile.models import Profile
from django.core import mail


def login(self, email: str, password: str):
    self.client.login(username=email, password=password)


def users_number():
    return User.objects.count()


def is_user_found(email: str):
    return User.objects.filter(email=email).exists()


def get_user(email: str):
    return User.objects.get(email=email)


def profiles_number():
    return Profile.objects.count()


def is_profile_found(user: User):
    return Profile.objects.filter(user_id=user.id).exists()


def get_profile(user: User):
    return Profile.objects.get(user_id=user.id)


def is_data_match(obj, data):
    for key, value in data.items():
        if not value == getattr(obj, key):
            return False

    return True


def emails_sent_number():
    return len(mail.outbox)


def get_mail(index: int):
    return mail.outbox[index]


def filter_dict(old_dict, keys):
    return {key: old_dict[key] for key in keys}
