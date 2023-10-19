from rest_framework.serializers import ValidationError


def validate_password_strength(password):
    min_length = 8
    if len(password) < 8:
        raise ValidationError(
            {"password": f"Hasło musi mieć minimum {min_length} znaki."}
        )

    if not any(char.isdigit() for char in password):
        raise ValidationError(
            {"password": "Hasło musi składać się z minimum jednej cyfry."}
        )

    if not any(char.isupper() for char in password):
        raise ValidationError(
            {"password": "Hasło musi składać się z minimum jednej dużej litery."}
        )


def validate_password_match(password, password2):
    if password != password2:
        raise ValidationError({"password2": "Hasła nie pasują."})


def validate_password_do_not_match(old_password, new_password):
    if old_password == new_password:
        raise ValidationError({"password": "Hasło nie może być takie jak poprzednie."})
