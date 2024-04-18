from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_coupon,
    create_coupon_obj,
    create_coupon_user,
)
from .helpers import login, coupons_number, is_data_match, get_coupon
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class CouponTest(APITestCase):
    def setUp(self):
        self.endpoint = "/coupons"
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
        self.admin_profile = create_profile(user=self.admin_user, user_type="A")
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
        self.profile = create_profile(user=self.user)

        self.coupon = create_coupon(
            "aaaaaaa",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon(
            "aaaaaab",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=11)),
        )
        create_coupon(
            "aaaaaav",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            "aaaaaad",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            "aaaaaae",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            "aaaaaag",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=5)),
        )

        self.new_coupon = create_coupon_obj(
            "new_coupon",
            20,
            True,
            True,
            [],
            True,
            1,
            1,
            True,
            make_aware(datetime.now() + timedelta(days=5)),
            10,
        )

        self.amend_coupon = create_coupon_obj(
            "new_coupon",
            10,
            True,
            False,
            [self.profile.id],
            True,
            1,
            1,
            True,
            make_aware(datetime.now() + timedelta(days=5)),
            10,
        )

    def test_get_coupons_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupons_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupons_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(coupons_number(), count)

    def test_get_coupon_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(self.coupon, data))

    def test_create_coupons_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_coupon
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 6)

    def test_create_coupons_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_coupon
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 6)

    def test_create_coupons_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_coupon
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(get_coupon(data["id"]), data))
        self.assertEqual(coupons_number(), 7)

    def test_update_coupons_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_coupons_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_coupons_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(get_coupon(data["id"]), data))

    def test_delete_coupons_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 6)

    def test_delete_coupons_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 6)

    def test_delete_coupons_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(coupons_number(), 5)


class CouponUserTest(APITestCase):
    def setUp(self):
        self.endpoint = "/coupon-usage"
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
        self.admin_profile = create_profile(user=self.admin_user, user_type="A")
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
        self.profile = create_profile(user=self.user)

        self.coupon_1 = create_coupon(
            "aaaaaaa",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=10)),
        )
        self.coupon_2 = create_coupon(
            "aaaaaab",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=11)),
        )
        self.coupon_3 = create_coupon(
            "aaaaaav",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            "aaaaaad",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            "aaaaaae",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            "aaaaaag",
            10,
            False,
            True,
            True,
            True,
            make_aware(datetime.now() + timedelta(days=5)),
        )

        self.coupon_user_1 = create_coupon_user(self.coupon_1, self.profile)
        self.coupon_user_2 = create_coupon_user(self.coupon_2, self.profile)
        self.coupon_user_3 = create_coupon_user(self.coupon_3, self.profile)

    def test_get_coupon_usage_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_usage_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_usage_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(coupons_number(), count)

    def test_get_coupon_usage_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_user_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_usage_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_user_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_usage_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_user_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
