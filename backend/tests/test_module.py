from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_lecturer_profile,
    create_lesson,
    create_technology,
    create_module,
    create_module_obj,
)
from .helpers import (
    login,
    is_data_match,
    get_lesson,
    get_module,
    modules_number,
    is_float,
)
from django.contrib import auth
import json


class ModuleTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/modules"
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

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
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

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
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

        self.module_3 = create_module(
            title="Module 3", lessons=[self.lesson_5, self.lesson_6]
        )

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

        self.new_module = create_module_obj(
            title="Javascript module",
            lessons=[self.lesson_1.id, self.lesson_4.id],
        )

        self.amend_module = create_module_obj(
            title=self.module_1.title,
            lessons=[self.lesson_2.id, self.lesson_5.id],
        )

    def test_get_modules_no_admin(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_modules_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 3)
        for module_data in results:
            lessons_data = module_data.pop("lessons")
            self.assertTrue(is_data_match(get_module(module_data["id"]), module_data))

            for lesson_data in lessons_data:
                self.assertTrue(
                    is_data_match(get_lesson(lesson_data["id"]), lesson_data)
                )

    def test_get_module_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.module_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_module_authorized_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.module_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_module_authorized(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.module_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        lessons_data = data.pop("lessons")

        self.assertTrue(is_data_match(get_module(data["id"]), data))

        for lesson_data in lessons_data:
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))

    def test_create_module_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_module
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(modules_number(), 3)

    def test_create_module_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_module
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(modules_number(), 3)

    def test_create_module_authorized(self):
        #  login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_module
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(modules_number(), 4)

        data = json.loads(response.content)

        lessons_ids = data.pop("lessons")
        self.assertTrue(is_data_match(get_module(data["id"]), data))
        self.assertTrue(lessons_ids, get_module(data["id"]).lessons)

    def test_update_module_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_module
        response = self.client.put(f"{self.endpoint}/{self.module_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(modules_number(), 3)

    def test_update_module_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_module
        response = self.client.put(f"{self.endpoint}/{self.module_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(modules_number(), 3)

    def test_update_module_authorized(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_module
        response = self.client.put(f"{self.endpoint}/{self.module_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modules_number(), 3)

        data = json.loads(response.content)

        lessons_ids = data.pop("lessons")
        self.assertTrue(is_data_match(get_module(data["id"]), data))
        self.assertTrue(lessons_ids, get_module(data["id"]).lessons)


class ModuleFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/modules"
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

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
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

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
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

        self.module_3 = create_module(
            title="Module 3", lessons=[self.lesson_5, self.lesson_6]
        )

    def test_title_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "title"
        variable = str(self.module_1.title)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class ModuleOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/modules"
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

        self.module_1 = create_module(title="Module 1", lessons=[self.lesson_1])

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
            title="Module 3", lessons=[self.lesson_5, self.lesson_6, self.lesson_2]
        )

        self.fields = ["title", "lessons_count"]

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
            self.assertEqual(count, 3)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
            elif "coupon_code" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "user_email" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "lessons_count" in field:
                field_values = [len(course["lessons"]) for course in results]
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
            self.assertEqual(count, 3)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
            elif "coupon_code" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "user_email" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "lessons_count" in field:
                field_values = [len(course["lessons"]) for course in results]
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
