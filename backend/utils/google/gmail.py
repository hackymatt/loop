from utils.google.service import build_service
from email.mime.text import MIMEText
import base64


class GmailApi:
    def __init__(self, on_behalf_of):
        scopes = ["https://www.googleapis.com/auth/gmail.send"]
        self.service = build_service(
            service_name="gmail",
            service_version="v1",
            on_behalf_of=on_behalf_of,
            scopes=scopes,
        )

    def _create_message(self, email_from, email_to, email_subject, email_body):
        message = MIMEText(email_body, "html")
        message["to"] = email_to
        message["from"] = f"loop.edu.pl <{email_from}>"
        message["subject"] = email_subject
        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def _send_message(self, user_id, message):
        message = (
            self.service.users().messages().send(userId=user_id, body=message).execute()
        )
        return message

    def send(self, email_from, email_to, email_subject, email_body):
        message = self._create_message(
            email_from=email_from,
            email_to=email_to,
            email_subject=email_subject,
            email_body=email_body,
        )
        return self._send_message("me", message=message)
