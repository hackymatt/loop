from django.contrib.auth.models import User
from profile.models import Profile, AdminProfile, LecturerProfile, StudentProfile
from course.models import Course
from coupon.models import Coupon
from certificate.models import Certificate
from lesson.models import Lesson
from technology.models import Technology
from topic.models import Topic
from tag.models import Tag
from review.models import Review
from module.models import Module
from newsletter.models import Newsletter
from notification.models import Notification
from message.models import Message
from schedule.models import Schedule, Recording
from reservation.models import Reservation
from teaching.models import Teaching
from cart.models import Cart
from wishlist.models import Wishlist
from post.models import Post, PostCategory
import uuid


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


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


def is_admin_profile_found(profile: Profile):
    return AdminProfile.objects.filter(profile=profile).exists()


def is_lecturer_profile_found(profile: Profile):
    return LecturerProfile.objects.filter(profile=profile).exists()


def is_student_profile_found(profile: Profile):
    return StudentProfile.objects.filter(profile=profile).exists()


def get_profile(user: User):
    return Profile.objects.get(user=user)


def get_admin_profile(profile: Profile):
    return AdminProfile.objects.get(profile=profile)


def get_lecturer_profile(profile: Profile):
    return LecturerProfile.objects.get(profile=profile)


def get_lecturer(id: int):
    return LecturerProfile.objects.get(pk=id)


def get_student_profile(profile: Profile):
    return StudentProfile.objects.get(profile=profile)


def is_data_match(obj, data):
    for key, value in data.items():
        data_value = str(value)
        obj_value = str(getattr(obj, key))
        if not data_value == obj_value:
            if key in ["modified_at", "created_at", "expiration_date"]:
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


def filter_dict(old_dict, keys):
    return {key: old_dict[key] for key in keys if key in old_dict}


def get_course(id: int):
    return Course.objects.get(pk=id)


def courses_number():
    return Course.objects.count()


def is_course_found(id: int):
    return Course.objects.filter(id=id).exists()


def get_course_modules(id: int):
    modules = Course.modules.through.objects.filter(course_id=id).values("module_id")
    return Module.lessons.through.objects.filter(module_id__in=modules)


def get_course_tags(id: int):
    return Course.tags.through.objects.filter(course_id=id)


def get_course_topics(id: int):
    return Course.topics.through.objects.filter(course_id=id)


def lessons_number():
    return Lesson.objects.count()


def modules_number():
    return Module.objects.count()


def get_lesson(id: int):
    return Lesson.objects.get(pk=id)


def get_module(id: int):
    return Module.objects.get(pk=id)


def technologies_number():
    return Technology.objects.count()


def topics_number():
    return Topic.objects.count()


def tags_number():
    return Tag.objects.count()


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


def get_tag(id: int):
    return Tag.objects.get(pk=id)


def get_topic(id: int):
    return Topic.objects.get(pk=id)


def get_schedules(lecturer: Profile):
    return Schedule.objects.filter(lecturer=lecturer).all()


def get_schedule(id: int):
    return Schedule.objects.get(pk=id)


def schedule_number():
    return Schedule.objects.count()


def is_schedule_found(id: int):
    return Schedule.objects.filter(id=id).exists()


def reservation_number():
    return Reservation.objects.count()


def is_reservation_found(id: int):
    return Reservation.objects.filter(id=id).exists()


def wishlist_number():
    return Wishlist.objects.count()


def cart_number():
    return Cart.objects.count()


def teaching_number():
    return Teaching.objects.count()


def coupons_number():
    return Coupon.objects.count()


def get_coupon(id: int):
    return Coupon.objects.get(pk=id)


def certificates_number():
    return Certificate.objects.count()


def notifications_number():
    return Notification.objects.count()


def recordings_number():
    return Recording.objects.count()


def messages_number():
    return Message.objects.count()


def post_categories_number():
    return PostCategory.objects.count()


def get_post_category(id: int):
    return PostCategory.objects.get(id=id)


def posts_number():
    return Post.objects.count()


def get_post(id: int):
    return Post.objects.get(id=id)


def mock_send_message(mock):
    mock.return_value = {}


def mock_create_event(mock):
    mock.return_value = {"id": str(uuid.uuid4()), "hangoutLink": "https://example.com"}


def mock_update_event(mock):
    mock.return_value = {"id": str(uuid.uuid4()), "hangoutLink": "https://example.com"}


def mock_delete_event(mock):
    mock.return_value = {}


def mock_get_recordings(mock, schedule_ids):
    data = [
        {
            "id": 1,
            "name": f"Dummy name",
            "webContentLink": f"https://example.com/1",
        }
    ]
    for schedule_id in schedule_ids:
        meeting_id = "{:07d}".format(schedule_id)
        id = str(uuid.uuid4())
        data.append(
            {
                "id": id,
                "name": f"Dummy name #{meeting_id}#",
                "webContentLink": f"https://example.com/{id}",
            }
        )

    mock.return_value = data


def mock_set_permissions(mock):
    mock.return_value = {}


def mock_register_payment(mock):
    mock.return_value = {"status_code": 200, "data": {"token": "token"}}


def mock_verify_payment(mock, result):
    mock.return_value = result
