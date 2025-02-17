from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_service,
    create_service_obj,
)
from .helpers import (
    login,
    is_data_match,
    get_service,
    services_number,
    is_float,
)
from django.contrib import auth
import json
from const import UserType


class ServiceTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/services"
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
            profile=create_profile(user=self.admin_user, user_type=UserType.ADMIN)
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

        self.service_1 = create_service(
            title="Python service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_2 = create_service(
            title="Python service 2",
            description="bbbb",
            price="2.99",
        )

        self.service_3 = create_service(
            title="JS service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_4 = create_service(
            title="JS service 2",
            description="bbbb",
            price="2.99",
        )

        self.service_5 = create_service(
            title="VBA service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_6 = create_service(
            title="VBA service 2",
            description="bbbb",
            price="2.99",
        )

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

        self.new_service = create_service_obj(
            title="Javascript course",
            description="service_description",
            price="89.99",
        )

        self.new_service_2 = create_service_obj(
            title="Javascript course",
            description="service_description",
            price="89.99",
            active=False,
        )

        self.amend_service = create_service_obj(
            title=self.service_1.title,
            description="service_description",
            price="19.99",
        )

        self.amend_service_2 = create_service_obj(
            title=self.service_1.title,
            description="service_description",
            price="19.99",
            active=False,
        )

    def test_get_services_no_admin(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_services_admin(self):
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
        for service_data in results:
            self.assertTrue(
                is_data_match(get_service(service_data["id"]), service_data)
            )

    def test_get_service_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.service_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_service_authorized_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.service_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_service_authorized_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.service_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertTrue(is_data_match(get_service(data["id"]), data))

    def test_create_service_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_service
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(services_number(), 6)

    def test_create_service_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_service
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(services_number(), 6)

    def test_create_service_authorized_1(self):
        #  login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_service
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(services_number(), 7)
        data = json.loads(response.content)
        self.assertTrue(is_data_match(get_service(data["id"]), data))

    def test_create_service_authorized_2(self):
        #  login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_service_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(services_number(), 7)
        data = json.loads(response.content)
        self.assertTrue(is_data_match(get_service(data["id"]), data))

    def test_update_service_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_service
        response = self.client.put(f"{self.endpoint}/{self.service_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(services_number(), 6)

    def test_update_service_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_service
        response = self.client.put(f"{self.endpoint}/{self.service_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(services_number(), 6)

    def test_update_service_authorized_price_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_service
        response = self.client.put(f"{self.endpoint}/{self.service_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(services_number(), 6)
        data = json.loads(response.content)
        self.assertTrue(is_data_match(get_service(data["id"]), data))

    def test_update_service_authorized_no_price_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_service_2
        data["price"] = self.service_1.price

        response = self.client.put(f"{self.endpoint}/{self.service_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(services_number(), 6)
        data = json.loads(response.content)
        self.assertTrue(is_data_match(get_service(data["id"]), data))


class ServiceFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/services"
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
            profile=create_profile(user=self.admin_user, user_type=UserType.ADMIN)
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

        self.service_1 = create_service(
            title="Python service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_2 = create_service(
            title="Python service 2",
            description="bbbb",
            price="2.99",
        )

        self.service_3 = create_service(
            title="JS service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_4 = create_service(
            title="JS service 2",
            description="bbbb",
            price="2.99",
        )

        self.service_5 = create_service(
            title="VBA service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_6 = create_service(
            title="VBA service 2",
            description="bbbb",
            price="2.99",
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

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.service_5.active = False
        self.service_5.save()

        active = "True"
        response = self.client.get(f"{self.endpoint}?active={active}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        actives = list(set([record["active"] for record in results]))
        self.assertTrue(len(actives) == 1)
        self.assertTrue(actives[0])


class ServiceOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/services"
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
            profile=create_profile(user=self.admin_user, user_type=UserType.ADMIN)
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

        self.service_1 = create_service(
            title="Python service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_2 = create_service(
            title="Python service 2",
            description="bbbb",
            price="2.99",
        )

        self.service_3 = create_service(
            title="JS service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_4 = create_service(
            title="JS service 2",
            description="bbbb",
            price="2.99",
        )

        self.service_5 = create_service(
            title="VBA service 1",
            description="bbbb",
            price="9.99",
        )

        self.service_6 = create_service(
            title="VBA service 2",
            description="bbbb",
            price="2.99",
        )

        self.fields = ["title", "price", "active"]

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
