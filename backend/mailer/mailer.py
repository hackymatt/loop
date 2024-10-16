from django.template.loader import render_to_string
from typing import List
from utils.google.gmail import GmailApi
from config_global import FRONTEND_URL, NOREPLY_EMAIL
from utils.logger.logger import logger


class Mailer:
    def __init__(self):
        self.gmail_api = GmailApi(on_behalf_of=NOREPLY_EMAIL)

    def send(self, email_template: str, to: List[str], subject: str, data):
        email_body = render_to_string(
            email_template,
            {
                **data,
                **{
                    "website_url": FRONTEND_URL,
                    "company": "loop",
                },
            },
        )
        try:
            self.gmail_api.send(
                NOREPLY_EMAIL,
                email_to=", ".join(to),
                email_subject=subject,
                email_body=email_body,
            )
        except Exception as e: # pragma: no cover
            logger.error(f"Błąd podczas wysyłania wiadomości: {e}", exc_info=True) # pragma: no cover
