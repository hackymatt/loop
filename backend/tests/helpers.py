from django.contrib.auth.models import User
from profile.models import Profile
from course.models import Course, Lesson, Skill, Topic
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
        if not str(value) == str(getattr(obj, key)):
            return False

    return True


def is_list_match(list_1, list_2):
    for d1, d2 in zip(list_1, list_2):
        for key, value in d1.items():
            if value != d2[key]:
                return False

    return True


def emails_sent_number():
    return len(mail.outbox)


def get_mail(index: int):
    return mail.outbox[index]


def filter_dict(old_dict, keys):
    return {key: old_dict[key] for key in keys}


def get_course(id: int):
    return Course.objects.get(pk=id)


def courses_number():
    return Course.objects.count()


def lessons_number():
    return Lesson.objects.count()


def get_lesson(id: int):
    return Lesson.objects.get(pk=id)


def get_skill(id: int):
    return Skill.objects.get(pk=id)


def get_topic(id: int):
    return Topic.objects.get(pk=id)
