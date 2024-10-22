from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_coupon,
    create_coupon_obj,
    create_coupon_user,
    create_payment,
)
from .helpers import (
    login,
    coupons_number,
    is_data_match,
    get_coupon,
    notifications_number,
    is_float,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class CouponTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupons"
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

        self.coupon = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon(
            code="aaaaaab",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        create_coupon(
            code="aaaaaav",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=10,
            is_infinite=False,
            all_users=True,
            is_percentage=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
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

        self.new_coupon_2 = create_coupon_obj(
            "new_coupon",
            20,
            True,
            False,
            [],
            True,
            1,
            1,
            True,
            make_aware(datetime.now() + timedelta(days=5)),
            10,
        )

        self.new_coupon_3 = create_coupon_obj(
            "new_coupon",
            20,
            True,
            False,
            [],
            True,
            1,
            1,
            False,
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

        self.amend_coupon_2 = create_coupon_obj(
            "new_coupon",
            10,
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

        self.amend_coupon_3 = create_coupon_obj(
            "new_coupon",
            10,
            True,
            True,
            [],
            True,
            1,
            1,
            False,
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
        # login
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
        # login
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
        self.assertEqual(coupons_number(), 7)
        self.assertEqual(notifications_number(), 0)

    def test_create_coupons_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_coupon
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 7)
        self.assertEqual(notifications_number(), 0)

    def test_create_coupons_authenticated_1(self):
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
        self.assertEqual(coupons_number(), 8)
        self.assertEqual(notifications_number(), 2)

    def test_create_coupons_authenticated_2(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_coupon_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(get_coupon(data["id"]), data))
        self.assertEqual(coupons_number(), 8)
        self.assertEqual(notifications_number(), 0)

    def test_create_coupons_authenticated_3(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_coupon_3
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(get_coupon(data["id"]), data))
        self.assertEqual(coupons_number(), 8)
        self.assertEqual(notifications_number(), 0)

    def test_update_coupons_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(notifications_number(), 0)

    def test_update_coupons_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(notifications_number(), 0)

    def test_update_coupons_authenticated_1(self):
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
        self.assertEqual(notifications_number(), 1)

    def test_update_coupons_authenticated_2(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon_2
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(get_coupon(data["id"]), data))
        self.assertEqual(notifications_number(), 2)

    def test_update_coupons_authenticated_3(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_coupon_3
        response = self.client.put(f"{self.endpoint}/{self.coupon.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        data.pop("users")
        self.assertTrue(is_data_match(get_coupon(data["id"]), data))
        self.assertEqual(notifications_number(), 0)

    def test_delete_coupons_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 7)

    def test_delete_coupons_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(coupons_number(), 7)

    def test_delete_coupons_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.coupon.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(coupons_number(), 6)


class CouponUserTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupon-usage"
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

        self.coupon_1 = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        self.coupon_2 = create_coupon(
            code="aaaaaab",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        self.coupon_3 = create_coupon(
            code="aaaaaav",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=10,
            is_infinite=False,
            all_users=True,
            is_percentage=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

        self.coupon_user_1 = create_coupon_user(
            self.coupon_1, self.profile, payment=create_payment(amount=1000)
        )
        self.coupon_user_2 = create_coupon_user(
            self.coupon_2, self.profile, payment=create_payment(amount=1000)
        )
        self.coupon_user_3 = create_coupon_user(
            self.coupon_3, self.profile, payment=create_payment(amount=1000)
        )

    def test_get_coupon_usage_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_coupon_usage_not_admin(self):
        # login
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
        # login
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


class CouponValidationTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupon-validate"
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
            first_name="first_name_2",
            last_name="last_name_2",
            email="email_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )

        self.coupon_1 = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        self.coupon_2 = create_coupon(
            code="aaaaaab",
            discount=10,
            is_percentage=False,
            all_users=False,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
            users=[self.profile_2.id],
        )

        self.coupon_3 = create_coupon(
            code="aaaaaac",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=False,
            max_uses=1,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon_user(
            coupon=self.coupon_3,
            user=self.profile_2,
            payment=create_payment(amount=1000),
        )

        self.coupon_4 = create_coupon(
            code="aaaaaae",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon_user(
            coupon=self.coupon_4, user=self.profile, payment=create_payment(amount=1000)
        )

        self.coupon_5 = create_coupon(
            code="aaaaaaf",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() - timedelta(days=10)),
        )

        self.coupon_6 = create_coupon(
            code="aaaaaag",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )

    def test_correct_validation(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_1.code}/20000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "discount": self.coupon_1.discount,
                "is_percentage": self.coupon_1.is_percentage,
            },
        )

    def test_coupon_not_found(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/notfound/200")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_not_for_user(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_2.code}/200")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_poll_empty(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_3.code}/200")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_user_max_usage(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_4.code}/200")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_expired(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_5.code}/200")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_inactive(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_6.code}/200")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_min_total(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.coupon_1.code}/50")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CouponFilteringTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupons"
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

        self.coupon = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon(
            code="aaaaaab",
            discount=11,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        create_coupon(
            code="aaaaaav",
            discount=12,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=14,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=41,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=4,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

    def test_code_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "code"
        variable = str(self.coupon.code)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "active"
        variable = True
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_discount_from_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "discount_from"
        variable = 10
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        values = list(set([variable <= record["discount"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_discount_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "discount_to"
        variable = 10
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        values = list(set([variable >= record["discount"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_expiration_date_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "expiration_date_to"
        variable = str(self.coupon.expiration_date)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        values = list(
            set([variable >= record["expiration_date"] for record in results])
        )
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class CouponUserFilteringTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupon-usage"
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

        self.coupon_1 = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        self.coupon_2 = create_coupon(
            code="aaaaaab",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        self.coupon_3 = create_coupon(
            code="aaaaaav",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=10,
            is_infinite=False,
            all_users=True,
            is_percentage=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

        self.coupon_user_1 = create_coupon_user(
            self.coupon_1, self.profile, payment=create_payment(amount=1000)
        )
        self.coupon_user_2 = create_coupon_user(
            self.coupon_2, self.profile, payment=create_payment(amount=1000)
        )
        self.coupon_user_3 = create_coupon_user(
            self.coupon_3, self.profile, payment=create_payment(amount=1000)
        )

    def test_user_id_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "user_id"
        variable = self.coupon_user_1.user.id
        response = self.client.get(f"{self.endpoint}")
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        values = list(set([variable == record["user"]["id"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_coupon_code_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "coupon_code"
        variable = self.coupon_1.code
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(
            set([variable in record["coupon"]["code"].lower() for record in results])
        )
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class CouponOrderingTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupons"
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

        self.coupon = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon(
            code="aaaaaab",
            discount=11,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        create_coupon(
            code="aaaaaav",
            discount=12,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=14,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=41,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=4,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

        self.fields = [
            "code",
            "discount",
            "active",
            "expiration_date",
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
            self.assertEqual(count, 7)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
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
            self.assertEqual(count, 7)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
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


class CouponUserOrderingTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupon-usage"
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

        self.coupon_1 = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        self.coupon_2 = create_coupon(
            code="aaaaaab",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        self.coupon_3 = create_coupon(
            code="aaaaaav",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=10,
            is_infinite=False,
            all_users=True,
            is_percentage=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

        self.coupon_user_1 = create_coupon_user(
            self.coupon_1, self.profile, payment=create_payment(amount=1000)
        )
        self.coupon_user_2 = create_coupon_user(
            self.coupon_2, self.profile, payment=create_payment(amount=1000)
        )
        self.coupon_user_3 = create_coupon_user(
            self.coupon_3, self.profile, payment=create_payment(amount=1000)
        )

        self.fields = [
            "coupon_code",
            "user_email",
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
