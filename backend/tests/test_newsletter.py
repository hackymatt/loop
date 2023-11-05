from rest_framework import status
from rest_framework.test import APITestCase
from .factory import create_newsletter
from .helpers import newsletters_number, get_newsletter, is_data_match
import json


class NewsletterEntriesTest(APITestCase):
    def setUp(self):
        self.endpoint = "/newsletter"

        self.active_newsletters = [
            create_newsletter(email=f"test_active_{i}@example.com") for i in range(15)
        ]
        self.inactive_newsletters = [
            create_newsletter(email=f"test_inactive_{i}@example.com", active=False)
            for i in range(5)
        ]

    def test_get_newsletter_entries(self):
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 20)

    def test_get_active_newsletter_entries(self):
        # get data
        response = self.client.get(f"{self.endpoint}?active=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 15)

    def test_get_inactive_newsletter_entries(self):
        # get data
        response = self.client.get(f"{self.endpoint}?active=False")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)

    def test_get_newsletter_entry(self):
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        newsletter = get_newsletter(uuid=self.active_newsletters[0].uuid)
        self.assertTrue(is_data_match(newsletter, data))


class NewsletterSubscribeTest(APITestCase):
    def setUp(self):
        self.endpoint = "/newsletter-subscribe"

    def test_subscribe_to_newsletter_without_history(self):
        # post data
        data = {"email": "test@example.com"}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(newsletters_number(), 1)

    def test_subscribe_to_newsletter_with_history(self):
        data = {"email": "test@example.com"}
        create_newsletter(email=data["email"], active=False)
        # post data
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(newsletters_number(), 1)


class NewsletterUnsubscribeTest(APITestCase):
    def setUp(self):
        self.endpoint = "/newsletter-unsubscribe"

        self.newsletter = create_newsletter(email="test@example.com")

    def test_unsubscribe_from_newsletter(self):
        # post data
        response = self.client.put(f"{self.endpoint}/{self.newsletter.uuid}", {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(get_newsletter(self.newsletter.uuid).active)
