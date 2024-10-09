from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_lecturer_profile,
    create_post_category,
    create_post,
    create_post_obj,
    create_image,
)
from .helpers import (
    login,
    posts_number,
    is_data_match,
    get_post,
    get_post_category,
    notifications_number,
)
from django.contrib import auth
import json
from base64 import b64encode


class PostTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/posts"
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

        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user = create_user(
            first_name="l1_first_name",
            last_name="l1_last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

        create_post_category(name="Technology")
        self.category = create_post_category(name="AI")
        create_post_category(name="Work")
        self.category_2 = create_post_category(name="Coding")
        create_post_category(name="Testing")

        self.post = create_post(
            title="abc",
            description="aaaa",
            content="bbbbbbbb",
            category=self.category,
            authors=[self.lecturer_profile],
        )
        create_post(
            title="abcd",
            description="aaaaa",
            content="bbbbbbbbb",
            category=self.category_2,
            authors=[self.lecturer_profile],
        )
        create_post(
            title="abc2",
            description="aaaa2",
            content="bbbbbbbb2",
            category=self.category,
            authors=[self.lecturer_profile],
        )
        self.post_2 = create_post(
            title="abcd2",
            description="aaaaa2",
            content="bbbbbbbbb2",
            category=self.category_2,
            authors=[self.lecturer_profile],
            active=False,
        )

        self.new_post = create_post_obj(
            title="Javascript post",
            description="post_description",
            content="post_content",
            category=self.category.id,
            authors=[self.lecturer_profile.id],
            image=b64encode(create_image().read()),
        )

        self.new_post_2 = create_post_obj(
            title="Javascript post",
            description="post_description",
            content="post_content",
            category=self.category_2.id,
            authors=[self.lecturer_profile.id],
            image=b64encode(create_image().read()),
            active=False,
        )

        self.amend_post = create_post_obj(
            title="Python for beginners post",
            description="post_description_other",
            content="post_content_other",
            category=self.category.id,
            authors=[self.lecturer_profile.id],
            image=b64encode(create_image().read()),
        )

        self.amend_post_2 = create_post_obj(
            title="Python for beginners post",
            description="post_description_other",
            content="post_content_other",
            category=self.category_2.id,
            authors=[self.lecturer_profile.id],
            image=b64encode(create_image().read()),
            active=False,
        )

    def test_get_posts_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertTrue(all("duration" in post.keys() for post in results))
        self.assertTrue(all("category" in post.keys() for post in results))
        self.assertTrue(all("authors" in post.keys() for post in results))
        self.assertEqual(count, 3)

    def test_get_posts_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertTrue(all("duration" in post.keys() for post in results))
        self.assertTrue(all("category" in post.keys() for post in results))
        self.assertTrue(all("authors" in post.keys() for post in results))
        self.assertEqual(count, 3)

    def test_get_posts_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertTrue(all("duration" in post.keys() for post in results))
        self.assertTrue(all("category" in post.keys() for post in results))
        self.assertTrue(all("authors" in post.keys() for post in results))
        self.assertEqual(count, 4)

    def test_get_post_inactive(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        self.post.active = False
        self.post.save()

        response = self.client.get(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_data = post_data.pop("category")
        duration = post_data.pop("duration")
        self.assertTrue(is_data_match(get_post(self.post.id), post_data))
        self.assertEqual(duration, 1)

        self.assertTrue(
            is_data_match(get_post_category(category_data["id"]), category_data)
        )

    def test_get_post_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_data = post_data.pop("category")
        duration = post_data.pop("duration")
        self.assertTrue(is_data_match(get_post(self.post.id), post_data))
        self.assertEqual(duration, 1)

        self.assertTrue(
            is_data_match(get_post_category(category_data["id"]), category_data)
        )

    def test_get_post_authenticated_2(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.post_2.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.post_2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_data = post_data.pop("category")
        duration = post_data.pop("duration")
        self.assertTrue(is_data_match(get_post(self.post_2.id), post_data))
        self.assertEqual(duration, 1)

        self.assertTrue(
            is_data_match(get_post_category(category_data["id"]), category_data)
        )

    def test_create_post_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_post
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_create_post_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_post
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_create_post_authenticated_1(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_post
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(posts_number(), 5)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_id = post_data.pop("category")
        self.assertTrue(is_data_match(get_post(post_data["id"]), post_data))
        self.assertEqual(category_id, data["category"])
        self.assertEqual(notifications_number(), 0)

    def test_create_post_authenticated_2(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_post_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(posts_number(), 5)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_id = post_data.pop("category")
        self.assertTrue(is_data_match(get_post(post_data["id"]), post_data))
        self.assertEqual(category_id, data["category"])
        self.assertEqual(notifications_number(), 0)

    def test_create_post_without_category(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_post
        del data["category"]
        data["category"] = []

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_create_post_without_authors(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_post
        del data["authors"]
        data["authors"] = []

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_update_post_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_post
        response = self.client.put(f"{self.endpoint}/{self.post.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_update_post_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_post
        response = self.client.put(f"{self.endpoint}/{self.post.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_update_post_authenticated_1(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_post
        response = self.client.put(f"{self.endpoint}/{self.post.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(posts_number(), 4)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_id = post_data.pop("category")
        self.assertTrue(is_data_match(get_post(post_data["id"]), post_data))
        self.assertEqual(category_id, data["category"])
        self.assertEqual(notifications_number(), 0)

    def test_update_post_authenticated_2(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_post_2
        response = self.client.put(f"{self.endpoint}/{self.post_2.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(posts_number(), 4)
        post_data = json.loads(response.content)
        post_data.pop("authors")
        category_id = post_data.pop("category")
        self.assertTrue(is_data_match(get_post(post_data["id"]), post_data))
        self.assertEqual(category_id, data["category"])
        self.assertEqual(notifications_number(), 0)

    def test_update_post_without_category(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_post
        del data["category"]
        data["category"] = []

        response = self.client.put(f"{self.endpoint}/{self.post.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_update_post_without_authors(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_post
        del data["authors"]
        data["authors"] = []

        response = self.client.put(f"{self.endpoint}/{self.post.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(posts_number(), 4)
        self.assertEqual(notifications_number(), 0)

    def test_delete_post_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        response = self.client.delete(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(posts_number(), 4)

    def test_delete_post_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        response = self.client.delete(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(posts_number(), 4)

    def test_delete_post_active_authorized(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        response = self.client.delete(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(posts_number(), 4)

    def test_delete_post_authorized(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        self.post.active = False
        self.post.save()

        response = self.client.delete(f"{self.endpoint}/{self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(posts_number(), 3)
