from django.db.models import TextChoices


class CertificateType(TextChoices):
    LESSON = "L", "Lekcja"
    MODULE = "M", "Moduł"
    COURSE = "K", "Kurs"


class CourseLevel(TextChoices):
    BASIC = "P", "Podstawowy"
    INTERMEDIATE = "Ś", "Średniozaawansowany"
    ADVANCED = "Z", "Zaawansowany"
    EXPERT = "E", "Ekspert"


class StatusType(TextChoices):
    NEW = "N", "NEW"
    READ = "R", "READ"


class GenderType(TextChoices):
    MALE = "M", "Mężczyzna"
    FEMALE = "K", "Kobieta"
    OTHER = "I", "Inne"


class UserType(TextChoices):
    STUDENT = "S", "Student"
    INSTRUCTOR = "W", "Wykładowca"
    ADMIN = "A", "Admin"
    OTHER = "I", "Inny"


class JoinType(TextChoices):
    EMAIL = "Email", "Email"
    GOOGLE = "Google", "Google"
    FACEBOOK = "Facebook", "Facebook"
    GITHUB = "GitHub", "GitHub"


class PaymentStatus(TextChoices):
    PENDING = "P", "Pending"
    SUCCESS = "S", "Success"
    FAILURE = "F", "Failure"


class CurrencyType(TextChoices):
    PLN = "PLN", "PLN"
    EUR = "EUR", "EUR"
    USD = "USD", "USD"


class PaymentMethod(TextChoices):
    PRZELEWY24 = "Przelewy24", "Przelewy24"
    PAYPAL = "PayPal", "PayPal"
    BANK_TRANSFER = "Przelew", "Przelew"
