from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings


def build_service(email_from, scopes):
    print(settings.GOOGLE_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(
        settings.GOOGLE_CREDENTIALS, scopes=scopes
    )
    delegated_credentials = credentials.with_subject(email_from)
    return build("gmail", "v1", credentials=delegated_credentials)
