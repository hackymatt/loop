from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.test import TestCase
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_admin_profile,
    create_other_profile,
    create_service,
    create_service_purchase as create_purchase,
    create_service_payment as create_payment,
    create_service_purchase_obj as create_purchase_obj,
)
from .helpers import (
    login,
    is_float,
    is_data_match,
    service_purchases_number as purchases_number,
)
import json
from django.contrib import auth


class PurchaseTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/service-purchases"
        self.client = APIClient()
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
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user_1))

        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="other@example.com",
            password=self.data["password"],
            is_active=False,
        )
        self.profile = create_other_profile(profile=create_profile(user=self.user_2))

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

        self.payment_1 = create_payment(
            amount=float(self.service_1.price) + float(self.service_2.price), status="P"
        )
        self.purchase_1 = create_purchase(
            service=self.service_1,
            other=self.profile,
            price=self.service_1.price,
            payment=self.payment_1,
        )
        self.purchase_2 = create_purchase(
            service=self.service_2,
            other=self.profile,
            price=self.service_2.price,
            payment=self.payment_1,
        )

        self.payment_2 = create_payment(
            amount=float(self.service_3.price)
            + float(self.service_4.price)
            + float(self.service_5.price),
            status="S",
        )
        self.purchase_3 = create_purchase(
            service=self.service_3,
            other=self.profile,
            price=self.service_3.price,
            payment=self.payment_2,
        )
        self.purchase_4 = create_purchase(
            service=self.service_4,
            other=self.profile,
            price=self.service_4.price,
            payment=self.payment_2,
        )
        self.purchase_5 = create_purchase(
            service=self.service_5,
            other=self.profile,
            price=self.service_5.price,
            payment=self.payment_2,
        )

        self.payment_3 = create_payment(amount=float(self.service_6.price), status="P")
        self.purchase_6 = create_purchase(
            service=self.service_6,
            other=self.profile,
            price=self.service_6.price,
            payment=self.payment_3,
        )

        self.payment_4 = create_payment(
            amount=float(self.service_6.price) + 50, status="P"
        )
        self.new_purchase = create_purchase_obj(
            service=self.service_6.id,
            other=self.profile.id,
            price=self.service_6.price,
            payment=self.payment_4.id,
        )
        self.edit_purchase = create_purchase_obj(
            service=self.service_1.id,
            other=self.profile.id,
            price=float(self.service_1.price) * 2,
            payment=self.payment_1.id,
        )

    def test_get_purchases_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_purchases_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_purchases_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        self.assertEqual(records_count, 6)

    def test_get_purchase_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.purchase_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_purchase_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.purchase_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_purchase_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.purchase_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        service = data.pop("service")
        payment = data.pop("payment")
        price = data.pop("price")
        self.assertEqual(price, self.purchase_1.price)
        self.assertTrue(is_data_match(self.purchase_1.service, service))
        self.assertEqual(payment, str(self.purchase_1.payment.session_id))

    def test_create_purchase_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_purchase
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(purchases_number(), 6)

    def test_create_purchase_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_purchase
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(purchases_number(), 6)

    def test_create_purchase_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_purchase
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(purchases_number(), 7)

    def test_create_purchase_service_inactive(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.service_6.active = False
        self.service_6.save()
        data = self.new_purchase
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(purchases_number(), 6)

    def test_create_purchase_payment_overextended(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.payment_4.amount = 1
        self.payment_4.save()
        data = self.new_purchase
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(purchases_number(), 6)

    def test_edit_purchase_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.edit_purchase
        response = self.client.put(f"{self.endpoint}/{self.purchase_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_purchase_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.edit_purchase
        response = self.client.put(f"{self.endpoint}/{self.purchase_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_purchase_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.payment_1.amount = self.payment_1.amount * 10
        self.payment_1.save()
        data = self.edit_purchase
        response = self.client.put(f"{self.endpoint}/{self.purchase_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service = data.pop("service")
        payment = data.pop("payment")
        price = data.pop("price")
        self.assertEqual(price, float(self.purchase_1.price) * 2)
        self.assertEqual(self.purchase_1.service.id, service)
        self.assertEqual(payment, self.purchase_1.payment.id)

    def test_delete_purchase_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        response = self.client.delete(f"{self.endpoint}/{self.purchase_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_purchase_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        response = self.client.delete(f"{self.endpoint}/{self.purchase_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_purchase_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        response = self.client.delete(f"{self.endpoint}/{self.purchase_1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(purchases_number(), 5)


class PurchaseFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/service-purchases"
        self.client = APIClient()
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
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=False,
        )
        self.profile = create_other_profile(profile=create_profile(user=self.user))

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

        self.payment_1 = create_payment(
            amount=float(self.service_1.price) + float(self.service_2.price), status="P"
        )
        create_purchase(
            service=self.service_1,
            other=self.profile,
            price=self.service_1.price,
            payment=self.payment_1,
        )
        create_purchase(
            service=self.service_2,
            other=self.profile,
            price=self.service_2.price,
            payment=self.payment_1,
        )

        self.payment_2 = create_payment(
            amount=float(self.service_3.price)
            + float(self.service_4.price)
            + float(self.service_5.price),
            status="S",
        )
        create_purchase(
            service=self.service_3,
            other=self.profile,
            price=self.service_3.price,
            payment=self.payment_2,
        )
        create_purchase(
            service=self.service_4,
            other=self.profile,
            price=self.service_4.price,
            payment=self.payment_2,
        )
        create_purchase(
            service=self.service_5,
            other=self.profile,
            price=self.service_5.price,
            payment=self.payment_2,
        )

        self.payment_3 = create_payment(amount=float(self.service_6.price), status="P")
        create_purchase(
            service=self.service_6,
            other=self.profile,
            price=self.service_6.price,
            payment=self.payment_3,
        )

    def test_service_title_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        service_title = self.service_1.title[1:5]
        response = self.client.get(f"{self.endpoint}?service_title={service_title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        titles = list(
            set([service_title in record["service"]["title"] for record in results])
        )
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

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.service_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class PurchaseOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/service-purchases"
        self.client = APIClient()
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
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=False,
        )
        self.profile = create_other_profile(profile=create_profile(user=self.user))

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

        self.payment_1 = create_payment(
            amount=float(self.service_1.price) + float(self.service_2.price), status="P"
        )
        create_purchase(
            service=self.service_1,
            other=self.profile,
            price=self.service_1.price,
            payment=self.payment_1,
        )
        create_purchase(
            service=self.service_2,
            other=self.profile,
            price=self.service_2.price,
            payment=self.payment_1,
        )

        self.payment_2 = create_payment(
            amount=float(self.service_3.price)
            + float(self.service_4.price)
            + float(self.service_5.price),
            status="S",
        )
        create_purchase(
            service=self.service_3,
            other=self.profile,
            price=self.service_3.price,
            payment=self.payment_2,
        )
        create_purchase(
            service=self.service_4,
            other=self.profile,
            price=self.service_4.price,
            payment=self.payment_2,
        )
        create_purchase(
            service=self.service_5,
            other=self.profile,
            price=self.service_5.price,
            payment=self.payment_2,
        )

        self.payment_3 = create_payment(amount=float(self.service_6.price), status="P")
        create_purchase(
            service=self.service_6,
            other=self.profile,
            price=self.service_6.price,
            payment=self.payment_3,
        )

        self.fields = [
            "service_title",
            "price",
            "created_at",
        ]

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
            if "_title" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course["reservation"]
                    for course in results
                    if course["reservation"] is not None
                ]
                parent_objects = [
                    course["schedule"]
                    for course in parent_objects
                    if course["schedule"] is not None
                ]
                parent_objects = [
                    course[field1]
                    for course in parent_objects
                    if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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
            self.assertEqual(count, 6)
            if "_title" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course["reservation"]
                    for course in results
                    if course["reservation"] is not None
                ]
                parent_objects = [
                    course["schedule"]
                    for course in parent_objects
                    if course["schedule"] is not None
                ]
                parent_objects = [
                    course[field1]
                    for course in parent_objects
                    if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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
