from django.db.models import TextChoices


class CertificateType(TextChoices):
    LESSON = "Lekcja"
    MODULE = "Moduł"
    COURSE = "Kurs"


class CourseLevel(TextChoices):
    BASIC = "Podstawowy"
    INTERMEDIATE = "Średniozaawansowany"
    ADVANCED = "Zaawansowany"
    EXPERT = "Ekspert"


class StatusType(TextChoices):
    NEW = "NEW"
    READ = "READ"


class GenderType(TextChoices):
    MALE = "Mężczyzna"
    FEMALE = "Kobieta"
    OTHER = "Inne"


class UserType(TextChoices):
    STUDENT = "Student"
    INSTRUCTOR = "Wykładowca"
    ADMIN = "Admin"
    OTHER = "Inny"


class JoinType(TextChoices):
    EMAIL = "Email"
    GOOGLE = "Google"
    FACEBOOK = "Facebook"
    GITHUB = "GitHub"


class PaymentStatus(TextChoices):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILURE = "Failure"


class CurrencyType(TextChoices):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


class PaymentMethod(TextChoices):
    PRZELEWY24 = "Przelewy24"
    PAYPAL = "PayPal"
    BANK_TRANSFER = "Przelew"
