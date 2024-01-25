from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from typing import List


class Mailer:
    def send(self, email_template: str, to: List[str], subject: str, data):
        message = render_to_string(email_template, data)
        email = EmailMultiAlternatives(subject, message, "from_email", to=to)
        email.attach_alternative(message, "text/html")

        return email.send()
