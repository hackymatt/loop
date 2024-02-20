from django.contrib.auth.models import User
from profile.models import Profile
from course.models import Course, Skill
from lesson.models import Lesson
from technology.models import Technology
from topic.models import Topic
from review.models import Review
from newsletter.models import Newsletter
from schedule.models import Schedule
from reservation.models import Reservation
from cart.models import Cart
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
    return Profile.objects.filter(user=user).exists()


def get_profile(user: User):
    return Profile.objects.get(user=user)


def is_data_match(obj, data):
    for key, value in data.items():
        data_value = str(value)
        obj_value = str(getattr(obj, key))
        if not data_value == obj_value:
            if key in ["modified_at", "created_at"]:
                modified_value = data_value.replace("T", " ")
                return modified_value[0:26] == obj_value[0:26]
            elif key in ["image", "video"]:
                modified_value = data_value.replace("http://testserver/media/", "")
                return modified_value == obj_value
            else:
                print(data_value, key, obj_value)
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
    return {key: old_dict[key] for key in keys if key in old_dict}


def get_course(id: int):
    return Course.objects.get(pk=id)


def courses_number():
    return Course.objects.count()


def is_course_found(id: int):
    return Course.objects.filter(id=id).exists()


def lessons_number():
    return Lesson.objects.count()


def get_lesson(id: int):
    return Lesson.objects.get(pk=id)


def technologies_number():
    return Technology.objects.count()


def topics_number():
    return Topic.objects.count()


def reviews_number():
    return Review.objects.count()


def newsletters_number():
    return Newsletter.objects.count()


def get_review(id: int):
    return Review.objects.get(pk=id)


def get_newsletter(uuid: str):
    return Newsletter.objects.get(uuid=uuid)


def is_review_found(id: int):
    return Review.objects.filter(id=id).exists()


def get_technology(id: int):
    return Technology.objects.get(pk=id)


def get_skill(id: int):
    return Skill.objects.get(pk=id)


def get_topic(id: int):
    return Topic.objects.get(pk=id)


def get_schedules(lecturer: Profile):
    return Schedule.objects.filter(lecturer=lecturer).all()


def reservation_number():
    return Reservation.objects.count()


def is_reservation_found(id: int):
    return Reservation.objects.filter(id=id).exists()


def cart_number():
    return Cart.objects.count()
