import string
import random


class VerificationCode:
    def __init__(self) -> None:
        self.VERIFICATION_CODE_TIMEOUT = 43200  # 12h
        self.VERIFICATION_CODE_LENGTH = 8
        self.CODE_CHARACTERS = (
            string.ascii_lowercase + string.ascii_uppercase + string.digits
        )

    def timeout(self):
        return self.VERIFICATION_CODE_TIMEOUT

    def generate(self):
        return "".join(
            random.choices(self.CODE_CHARACTERS, k=self.VERIFICATION_CODE_LENGTH)
        )
