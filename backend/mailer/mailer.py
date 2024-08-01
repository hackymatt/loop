from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from typing import List
from django.conf import settings
from utils.google.gmail import GmailApi


class Mailer:
    def __init__(self):
        self.gmail_api = GmailApi(email_from=settings.EMAIL_FROM)

    def send(self, email_template: str, to: List[str], subject: str, data):
        email_body = render_to_string(
            email_template,
            {
                **data,
                **{
                    "website_url": settings.BASE_FRONTEND_URL,
                    "company": "loop",
                },
            },
        )
        return self.gmail_api.send(
            settings.EMAIL_FROM,
            email_to=", ".join(to),
            email_subject=subject,
            email_body=email_body,
        )
