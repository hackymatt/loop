from purchase.models import Payment, ServicePurchase, Purchase
from lesson.models import Lesson
from mailer.mailer import Mailer
from config_global import CONTACT_EMAIL, ACCOUNT_NUMBER
from purchase.invoice import Invoice
from typing import List
from math import floor
from notification.utils import notify


def get_lessons_price(lessons):
    for lesson_data in lessons:
        id = lesson_data["lesson"]
        lesson = Lesson.objects.get(id=id)
        lesson_data["price"] = lesson.price

    return lessons


def get_total_price(lessons):
    return max(sum([float(lesson["price"]) for lesson in lessons]), 0)


def get_discounted_total(total_price, coupon_details):
    if coupon_details["is_percentage"]:
        return (
            floor(
                max(float(total_price) * (1 - coupon_details["discount"] / 100), 0)
                * 100
            )
            / 100
        )

    return floor(max(total_price - coupon_details["discount"], 0) * 100) / 100


def get_discount_percentage(lessons, coupon_details):
    if coupon_details["is_percentage"]:
        return coupon_details["discount"]

    total_price = get_total_price(lessons=lessons)
    discounted_total_price = total_price - coupon_details["discount"]
    return (1 - discounted_total_price / total_price) * 100


def discount_lesson_price(lessons, discount_percentage):
    new_lessons = []
    for lesson in lessons:
        new_lesson = lesson.copy()
        original_price = lesson["price"]
        new_price = float(original_price) * (1 - discount_percentage / 100)
        new_lesson["price"] = floor(max(new_price, 0) * 100) / 100
        new_lessons.append(new_lesson)

    return new_lessons


def confirm_service_purchase(purchases: List[ServicePurchase], payment: Payment):
    payment_successful = payment.status == "S"
    payment_rejected = payment.status == "F"

    amount = payment.amount / 100
    currency = payment.currency

    purchase = purchases[0]

    mailer = Mailer()
    mail_data = {
        **{
            "title": "Płatność utworzona",
            "description": "Poniżej przedstawione szczegóły zakupu.",
            "lessons": [purchase.service.title for purchase in purchases],
            "amount": f"{amount:,.2f} {currency}",
            "status": "Utworzona",
        }
    }

    attachments = []

    customer = {
        "id": purchase.other.id,
        "full_name": f"{purchase.other.profile.user.first_name} {purchase.other.profile.user.last_name}",
        "street_address": purchase.other.profile.street_address,
        "city": purchase.other.profile.city,
        "zip_code": purchase.other.profile.zip_code,
        "country": purchase.other.profile.country,
    }
    items = [
        {
            "id": purchase.service.id,
            "name": purchase.service.title,
            "price": purchase.service.price,
        }
        for purchase in purchases
    ]
    notes = payment.notes
    payment = {
        "id": payment.id,
        "amount": payment.amount / 100,
        "currency": payment.currency,
        "status": "Zapłacono" if payment_successful else "Do zapłaty",
        "method": payment.method,
        "account": ACCOUNT_NUMBER if payment.method == "Przelew" else None,
    }
    invoice = Invoice(customer=customer, items=items, payment=payment, notes=notes)
    if not payment_rejected:
        invoice_path = invoice.create()
        attachments = [invoice_path]
        invoice.upload()

    mailer.send(
        email_template="purchase_confirmation.html",
        to=[CONTACT_EMAIL],
        subject="Podsumowanie zakupu",
        data=mail_data,
        attachments=attachments,
    )

    if not payment_rejected:
        invoice.remove()


def confirm_purchase(purchases, payment: Payment):
    payment_successful = payment.status == "S"

    title = (
        "Twój zakup jest zakończony!"
        if payment_successful
        else "Twój zakup nie powiódł się."
    )
    description = (
        "Przejdź do swojego konta i zarezerwuj termin."
        if payment_successful
        else "Przejdź do koszyka i ponów płatność."
    )
    path = (
        "/account/lessons?sort_by=-created_at&page_size=10"
        if payment_successful
        else "/cart"
    )
    amount = payment.amount / 100
    currency = payment.currency

    purchase = purchases[0]

    notify(
        profile=purchase.student.profile,
        title=title,
        subtitle=f"Ilość lekcji: {purchases.count()}",
        description=description,
        path=path,
        icon="mdi:shopping",
    )

    mailer = Mailer()
    mail_data = {
        **{
            "title": title,
            "description": description,
            "lessons": [purchase.lesson.title for purchase in purchases],
            "amount": f"{amount:,.2f} {currency}",
            "status": "Otrzymana" if payment_successful else "Odrzucona",
        }
    }

    attachments = []

    customer = {
        "id": purchase.student.id,
        "full_name": f"{purchase.student.profile.user.first_name} {purchase.student.profile.user.last_name}",
        "street_address": purchase.student.profile.street_address,
        "city": purchase.student.profile.city,
        "zip_code": purchase.student.profile.zip_code,
        "country": purchase.student.profile.country,
    }
    items = [
        {
            "id": purchase.lesson.id,
            "name": purchase.lesson.title,
            "price": purchase.lesson.price,
        }
        for purchase in purchases
    ]
    payment = {
        "id": payment.id,
        "amount": payment.amount / 100,
        "currency": payment.currency,
        "status": "Zapłacono" if payment_successful else "Do zapłaty",
        "method": payment.method,
        "account": "",
    }
    notes = ""
    invoice = Invoice(customer=customer, items=items, payment=payment, notes=notes)
    if payment_successful:
        invoice_path = invoice.create()
        attachments = [invoice_path]
        invoice.upload()

    mailer.send(
        email_template="purchase_confirmation.html",
        to=[purchase.student.profile.user.email],
        subject="Podsumowanie zakupu",
        data=mail_data,
        attachments=attachments,
    )

    if payment_successful:
        invoice.remove()
