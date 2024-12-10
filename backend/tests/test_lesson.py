from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_lecturer_profile,
    create_lesson,
    create_lesson_obj,
    create_technology,
    create_review,
    create_purchase,
    create_teaching,
    create_lesson_price_history,
    create_payment,
    create_topic,
    create_candidate,
    create_tag,
    create_course,
    create_module,
)
from .helpers import (
    login,
    is_data_match,
    get_lesson,
    filter_dict,
    get_technology,
    lessons_number,
    notifications_number,
    get_lecturer,
    is_float,
)
from django.contrib import auth
import json


class LessonTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lessons"
        self.admin_data = {
            "email": "admin_test_email@example.com",
            "password": "TestPassword123",
        }
        self.admin_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.admin_data["email"],
            password=self.admin_data["password"],
            is_active=True,
            is_staff=True,
        )
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )

        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )

        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        self.review_4 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_5 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_3],
        )

        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_5,
            student=self.profile,
            price=self.lesson_5.price,
            payment=create_payment(amount=self.lesson_5.price),
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
            payment=create_payment(amount=self.lesson_6.price),
        )

        self.review_6 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_7 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

        self.new_lesson = create_lesson_obj(
            title="Javascript course",
            description="lesson_description",
            price="89.99",
            duration=90,
            github_url="https://github.com/loopedupl/lesson",
            technologies=[self.technology_2.id],
        )

        self.new_lesson_2 = create_lesson_obj(
            title="Javascript course",
            description="lesson_description",
            price="89.99",
            duration=90,
            github_url="https://github.com/loopedupl/lesson",
            technologies=[self.technology_2.id],
            active=False,
        )

        self.amend_lesson = create_lesson_obj(
            title=self.lesson_1.title,
            description="lesson_description",
            price="19.99",
            duration=60,
            github_url="https://github.com/loopedupl/lesson",
            technologies=[self.technology_1.id],
        )

        self.amend_lesson_2 = create_lesson_obj(
            title=self.lesson_1.title,
            description="lesson_description",
            price="19.99",
            duration=60,
            github_url="https://github.com/loopedupl/lesson",
            technologies=[self.technology_1.id],
            active=False,
        )

    def test_get_lessons_no_admin(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lessons_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 6)
        for lesson_data in results:
            technologies_data = lesson_data.pop("technologies")
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
            elif (
                lesson_data["id"] == self.review_2.lesson.id
                or lesson_data["id"] == self.review_3.lesson.id
                or lesson_data["id"] == self.review_5.lesson.id
                or lesson_data["id"] == self.review_7.lesson.id
            ):
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
            elif (
                lesson_data["id"] == self.review_4.lesson.id
                or lesson_data["id"] == self.review_6.lesson.id
            ):
                self.assertEqual(rating, 4.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)

            for technology_data in technologies_data:
                self.assertTrue(
                    is_data_match(
                        get_technology(technology_data["id"]), technology_data
                    )
                )

            for lecturer_data in lecturers_data:
                user_data = filter_dict(lecturer_data, self.user_columns)
                profile_data = filter_dict(lecturer_data, self.profile_columns)
                self.assertTrue(
                    is_data_match(get_lecturer(lecturer_data["id"]), user_data)
                )
                self.assertTrue(
                    is_data_match(
                        get_lecturer(lecturer_data["id"]).profile, profile_data
                    )
                )

    def test_get_lesson_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.lesson_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        technologies_data = data.pop("technologies")
        lecturers_data = data.pop("lecturers")
        rating = data.pop("rating")
        rating_count = data.pop("rating_count")
        students_count = data.pop("students_count")

        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)

        for technology_data in technologies_data:
            self.assertTrue(
                is_data_match(get_technology(technology_data["id"]), technology_data)
            )

        for lecturer_data in lecturers_data:
            user_data = filter_dict(lecturer_data, self.user_columns)
            profile_data = filter_dict(lecturer_data, self.profile_columns)
            self.assertTrue(is_data_match(get_lecturer(lecturer_data["id"]), user_data))
            self.assertTrue(
                is_data_match(get_lecturer(lecturer_data["id"]).profile, profile_data)
            )

    def test_get_lesson_authorized(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.review_1.delete()
        self.review_2.delete()
        response = self.client.get(f"{self.endpoint}/{self.lesson_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        technologies_data = data.pop("technologies")
        lecturers_data = data.pop("lecturers")
        rating = data.pop("rating")
        rating_count = data.pop("rating_count")
        students_count = data.pop("students_count")

        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertEqual(rating, None)
        self.assertEqual(rating_count, 0)
        self.assertEqual(students_count, 1)

        for technology_data in technologies_data:
            self.assertTrue(
                is_data_match(get_technology(technology_data["id"]), technology_data)
            )

        for lecturer_data in lecturers_data:
            user_data = filter_dict(lecturer_data, self.user_columns)
            profile_data = filter_dict(lecturer_data, self.profile_columns)
            self.assertTrue(is_data_match(get_lecturer(lecturer_data["id"]), user_data))
            self.assertTrue(
                is_data_match(get_lecturer(lecturer_data["id"]).profile, profile_data)
            )

    def test_create_lesson_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_lesson
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

    def test_create_lesson_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_lesson
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

    def test_create_lesson_incorrect_duration(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_lesson
        data["duration"] = 55
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

    def test_create_lesson_incorrect_github_url(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_lesson
        data["github_url"] = "https://github.com/test/lesson"
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

    def test_create_lesson_authorized_1(self):
        #  login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_lesson
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(lessons_number(), 7)

        data = json.loads(response.content)

        technologies_ids = data.pop("technologies")
        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertTrue(technologies_ids, get_lesson(data["id"]).technologies)
        self.assertEqual(notifications_number(), 3)

    def test_create_lesson_authorized_2(self):
        #  login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_lesson_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(lessons_number(), 7)

        data = json.loads(response.content)

        technologies_ids = data.pop("technologies")
        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertTrue(technologies_ids, get_lesson(data["id"]).technologies)
        self.assertEqual(notifications_number(), 0)

    def test_update_lesson_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_lesson
        response = self.client.put(f"{self.endpoint}/{self.lesson_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

    def test_update_lesson_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_lesson
        response = self.client.put(f"{self.endpoint}/{self.lesson_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

    def test_update_lesson_authorized_price_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_lesson
        response = self.client.put(f"{self.endpoint}/{self.lesson_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 3)

        data = json.loads(response.content)

        technologies_ids = data.pop("technologies")
        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertTrue(technologies_ids, get_lesson(data["id"]).technologies)

    def test_update_lesson_authorized_no_price_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_lesson_2
        data["price"] = self.lesson_1.price

        response = self.client.put(f"{self.endpoint}/{self.lesson_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(lessons_number(), 6)
        self.assertEqual(notifications_number(), 0)

        data = json.loads(response.content)

        technologies_ids = data.pop("technologies")
        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertTrue(technologies_ids, get_lesson(data["id"]).technologies)


class LessonFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lessons"
        self.admin_data = {
            "email": "admin_test_email@example.com",
            "password": "TestPassword123",
        }
        self.admin_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.admin_data["email"],
            password=self.admin_data["password"],
            is_active=True,
            is_staff=True,
        )
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )

        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )

        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        self.review_4 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_5 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lasson",
            price="2.99",
            technologies=[self.technology_3],
        )

        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_5,
            student=self.profile,
            price=self.lesson_5.price,
            payment=create_payment(amount=self.lesson_5.price),
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
            payment=create_payment(amount=self.lesson_6.price),
        )

        self.review_6 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_7 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

    def test_title_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        title = "pyth"
        response = self.client.get(f"{self.endpoint}?title={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        titles = list(set([title in record["title"].lower() for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_duration_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        duration = 40
        response = self.client.get(f"{self.endpoint}?duration_from={duration}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        durations = list(set([record["duration"] >= duration for record in results]))
        self.assertTrue(len(durations) == 1)
        self.assertTrue(durations[0])

    def test_duration_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        duration = 30
        response = self.client.get(f"{self.endpoint}?duration_to={duration}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        durations = list(set([record["duration"] <= duration for record in results]))
        self.assertTrue(len(durations) == 1)
        self.assertTrue(durations[0])

    def test_price_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 5
        response = self.client.get(f"{self.endpoint}?price_from={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        prices = list(set([float(record["price"]) >= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_price_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 10
        response = self.client.get(f"{self.endpoint}?price_to={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        prices = list(set([float(record["price"]) <= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_github_url_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        github_url = "lesson"
        response = self.client.get(f"{self.endpoint}?github_url={github_url}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        github_urls = list(
            set([github_url in record["github_url"] for record in results])
        )
        self.assertTrue(len(github_urls) == 1)
        self.assertTrue(github_urls[0])

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.lesson_5.active = True
        self.lesson_5.save()

        active = "True"
        response = self.client.get(f"{self.endpoint}?active={active}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        actives = list(set([record["active"] for record in results]))
        self.assertTrue(len(actives) == 1)
        self.assertTrue(actives[0])


class LessonOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lessons"
        self.admin_data = {
            "email": "admin_test_email@example.com",
            "password": "TestPassword123",
        }
        self.admin_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.admin_data["email"],
            password=self.admin_data["password"],
            is_active=True,
            is_staff=True,
        )
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )

        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )

        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        self.review_4 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_5 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lasson",
            price="2.99",
            technologies=[self.technology_3],
        )

        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_5,
            student=self.profile,
            price=self.lesson_5.price,
            payment=create_payment(amount=self.lesson_5.price),
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
            payment=create_payment(amount=self.lesson_6.price),
        )

        self.review_6 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_7 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.fields = ["title", "duration", "price", "github_url", "active"]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 6)
            field_values = [course[field] for course in results]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values, sorted(field_values, key=lambda d: d["name"])
                )
            else:
                field_values = [
                    field_value if not is_float(field_value) else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values))
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by=-{field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 6)
            field_values = [course[field] for course in results]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values,
                    sorted(field_values, key=lambda d: d["name"], reverse=True),
                )
            else:
                field_values = [
                    field_value if not is_float(field_value) else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values, reverse=True))


class LessonPriceHistoryFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lesson-price-history"
        self.admin_data = {
            "email": "admin_test_email@example.com",
            "password": "TestPassword123",
        }
        self.admin_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.admin_data["email"],
            password=self.admin_data["password"],
            is_active=True,
            is_staff=True,
        )
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.candidate_1 = create_candidate(name="No tech knowledge")
        self.candidate_2 = create_candidate(name="Tech interested")

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course = create_course(
            title="course_title",
            description="course_description",
            overview="course_overview",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_1],
        )

        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )
        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
        )

        self.course_2 = create_course(
            title="course_title 2",
            description="course_description",
            overview="course_overview",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_2],
        )

        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )
        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_3],
        )
        self.module_3 = create_module(
            title="Module 3", lessons=[self.lesson_5, self.lesson_6]
        )

        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            overview="course_overview",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_3],
        )

        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

    def test_lesson_name_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        title = self.lesson_1.title[0:5]
        response = self.client.get(f"{self.endpoint}?lesson_name={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        titles = list(set([title in record["lesson"]["title"] for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_price_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 5
        response = self.client.get(f"{self.endpoint}?price_from={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 12)
        prices = list(set([float(record["price"]) >= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_price_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 10
        response = self.client.get(f"{self.endpoint}?price_to={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 12)
        prices = list(set([float(record["price"]) <= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.lesson_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 18)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class LessonPriceHistoryOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lesson-price-history"
        self.admin_data = {
            "email": "admin_test_email@example.com",
            "password": "TestPassword123",
        }
        self.admin_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.admin_data["email"],
            password=self.admin_data["password"],
            is_active=True,
            is_staff=True,
        )
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.candidate_1 = create_candidate(name="No tech knowledge")
        self.candidate_2 = create_candidate(name="Tech interested")

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course = create_course(
            title="course_title",
            description="course_description",
            overview="course_overview",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_1],
        )

        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )
        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
        )

        self.course_2 = create_course(
            title="course_title 2",
            description="course_description",
            overview="course_overview",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_2],
        )

        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )
        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_3],
        )

        self.module_3 = create_module(
            title="Module 3", lessons=[self.lesson_5, self.lesson_6]
        )

        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            overview="course_overview",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_3],
        )

        create_lesson_price_history(self.lesson_6, 15)
        create_lesson_price_history(self.lesson_6, 25)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

        self.fields = ["lesson_name", "price", "created_at"]

    def test_ordering(self):
        for field in self.fields:
            # login
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 18)
            if field == "lesson_name":
                field_values = [course["lesson"]["title"] for course in results]
            else:
                field_values = [course[field] for course in results]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values, sorted(field_values, key=lambda d: d["name"])
                )
            else:
                field_values = [
                    field_value if not is_float(field_value) else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values))
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by=-{field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 18)
            if field == "lesson_name":
                field_values = [course["lesson"]["title"] for course in results]
            else:
                field_values = [course[field] for course in results]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values,
                    sorted(field_values, key=lambda d: d["name"], reverse=True),
                )
            else:
                field_values = [
                    field_value if not is_float(field_value) else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values, reverse=True))
