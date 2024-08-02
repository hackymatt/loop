from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings


def build_service(service_name, service_version, email_from, scopes):
    credentials = service_account.Credentials.from_service_account_info(
        settings.GOOGLE_CREDENTIALS, scopes=scopes
    )
    delegated_credentials = credentials.with_subject(email_from)
    return build(service_name, service_version, credentials=delegated_credentials)
