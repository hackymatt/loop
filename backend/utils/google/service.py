from google.oauth2 import service_account
from googleapiclient.discovery import build
from config_global import GOOGLE_CREDENTIALS


def build_service(service_name, service_version, on_behalf_of, scopes):
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS, scopes=scopes
    )
    delegated_credentials = credentials.with_subject(on_behalf_of)
    return build(service_name, service_version, credentials=delegated_credentials)
