from rest_framework import status
from rest_framework.test import APIClient

from .factory import create_image, create_newsletter, create_user, create_profile
from .helpers import notifications_number

from django.test import TestCase
from unittest.mock import patch, Mock

from base64 import b64encode


class LoginGithubTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/login-github"
        self.client = APIClient()

        self.data = {"code": "test_code"}

    def mock_github_get_access_token_request(self, mock, success):
        mock_response = Mock()
        mock_response.ok = success
        if success:
            mock_response.json.return_value = {"access_token": "token"}
        mock.return_value = mock_response

    def mock_github_get_user_email_request(self, mock, success):
        mock_response = Mock()
        mock_response.ok = success
        if success:
            mock_response.json.return_value = [
                {
                    "email": "email",
                    "primary": True,
                },
                {
                    "email": "email2",
                    "primary": False,
                },
            ]
        mock.return_value = mock_response

    def mock_github_get_user_info_request(self, mock, success, info=None):
        mock_response = Mock()
        mock_response.ok = success
        if success:
            if not info:
                info = {
                    "login": "login",
                    "avatar_url": "https:www.example.com/image",
                }
            mock_response.json.return_value = info
        mock.return_value = mock_response

    def mock_get_image_content_request(self, mock, success):
        mock_response = Mock()
        mock_response.ok = success
        if success:
            mock_response.content = b64encode(create_image().read())
        mock.return_value = mock_response

    def test_missing_code(self):
        response = self.client.post(self.endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("profile.login.utils.github_get_access_token_request")
    def test_get_token_error(self, github_get_access_token_request_mock):
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=False
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_get_user_email_error(
        self, github_get_access_token_request_mock, github_get_user_email_request_mock
    ):
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=False
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_get_user_info_error(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
    ):
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock, success=False
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("profile.login.utils.get_image_content_request")
    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_get_image_content_error(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
        get_image_content_request_mock,
    ):
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock, success=True
        )
        self.mock_get_image_content_request(
            mock=get_image_content_request_mock, success=False
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("profile.login.utils.get_image_content_request")
    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_success_full_data(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
        get_image_content_request_mock,
    ):
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock, success=True
        )
        self.mock_get_image_content_request(
            mock=get_image_content_request_mock, success=True
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications_number(), 1)

    @patch("profile.login.utils.get_image_content_request")
    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_success_without_image(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
        get_image_content_request_mock,
    ):
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock,
            success=True,
            info={
                "login": "login",
                "avatar_url": "",
            },
        )
        self.mock_get_image_content_request(
            mock=get_image_content_request_mock, success=True
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications_number(), 1)

    @patch("profile.login.utils.get_image_content_request")
    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_success_with_previous_newsletter(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
        get_image_content_request_mock,
    ):
        create_newsletter(email="email")
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock,
            success=True,
        )
        self.mock_get_image_content_request(
            mock=get_image_content_request_mock, success=True
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications_number(), 1)

    @patch("profile.login.utils.get_image_content_request")
    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_success_with_previous_account_lecturer(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
        get_image_content_request_mock,
    ):
        create_profile(
            user=create_user("first_name", "last_name", "email", "abcdef1!", True),
            user_type="W",
        )
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock,
            success=True,
        )
        self.mock_get_image_content_request(
            mock=get_image_content_request_mock, success=True
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications_number(), 0)

    @patch("profile.login.utils.get_image_content_request")
    @patch("profile.login.utils.github_get_user_info_request")
    @patch("profile.login.utils.github_get_user_email_request")
    @patch("profile.login.utils.github_get_access_token_request")
    def test_success_with_previous_account_admin(
        self,
        github_get_access_token_request_mock,
        github_get_user_email_request_mock,
        github_get_user_info_request_mock,
        get_image_content_request_mock,
    ):
        create_profile(
            user=create_user("first_name", "last_name", "email", "abcdef1!", True),
            user_type="A",
        )
        self.mock_github_get_access_token_request(
            mock=github_get_access_token_request_mock, success=True
        )
        self.mock_github_get_user_email_request(
            mock=github_get_user_email_request_mock, success=True
        )
        self.mock_github_get_user_info_request(
            mock=github_get_user_info_request_mock,
            success=True,
        )
        self.mock_get_image_content_request(
            mock=get_image_content_request_mock, success=True
        )
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications_number(), 0)
