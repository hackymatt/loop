from rest_framework.serializers import ValidationError
from const import MIN_PASSWORD_LENGTH


def validate_password_strength(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            {"password": f"Hasło musi mieć minimum {MIN_PASSWORD_LENGTH} znaków."}
        )

    if not any(char.isdigit() for char in password):
        raise ValidationError(
            {"password": "Hasło musi składać się z minimum jednej cyfry."}
        )

    if not any(char.isupper() for char in password):
        raise ValidationError(
            {"password": "Hasło musi składać się z minimum jednej dużej litery."}
        )

    if not any(char.islower() for char in password):
        raise ValidationError(
            {"password": "Hasło musi składać się z minimum jednej małej litery."}
        )

    if all(char.isalpha() or char.isdigit() for char in password):
        raise ValidationError(
            {"password": "Hasło musi składać się z minimum jednego znaku specjalnego."}
        )


def validate_password_match(password, password2):
    if password != password2:
        raise ValidationError({"password2": "Hasła nie pasują."})


def validate_password_do_not_match(old_password, new_password):
    if old_password == new_password:
        raise ValidationError({"password": "Hasło nie może być takie jak poprzednie."})
