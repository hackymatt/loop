from django.db.models import Sum
from django.template.loader import render_to_string
from datetime import date, datetime
from purchase.models import Payment
from config_global import VAT_RATE, VAT_LIMIT, FRONTEND_URL, IS_LOCAL, STORAGES
from weasyprint import HTML
import os
from collections import defaultdict
from django.core.files.storage import get_storage_class
from utils.logger.logger import logger


class Invoice:
    def __init__(self, customer, items, payment, notes):
        self.PRODUCT_TYPE = "szt."
        self.INVOICE_DIR = "invoices"
        self.items = self.group_items(items=items)
        self.payment = payment
        self.notes = notes
        self.date = date.today()
        self.is_vat = self._is_vat()
        self.vat_rate = VAT_RATE if self.is_vat else 0
        self.invoice_number = self.get_invoice_number(self.payment["id"])
        self.customer = customer
        self.filename = f"{self.invoice_number}.pdf"
        self.path = os.path.join(self.INVOICE_DIR, self.filename)

        self.data = {
            "vat": self.is_vat,
            "invoice_date": self.date,
            "invoice_number": self.invoice_number,
            "customer": {
                "full_name": self.customer["full_name"],
                "id": self._format_id(id=self.customer["id"]),
                "street": self.customer["street_address"],
                "city": self.customer["city"],
                "zip_code": self.customer["zip_code"],
                "country": self.customer["country"],
            },
            "products": [
                {
                    "id": self._format_id(id=item["id"]),
                    "name": item["name"],
                    "type": self.PRODUCT_TYPE,
                    "quantity": item["quantity"],
                    "price_netto": self._format_number(
                        number=self._calc_net_price(price=item["price"])
                    ),
                    "subtotal_netto": self._format_number(
                        number=self._calc_net_subtotal(
                            price=item["price"], quantity=item["quantity"]
                        )
                    ),
                    "vat_percent": f"{self.vat_rate}%",
                    "vat": self._format_number(
                        number=self._calc_vat(price=item["price"])
                    ),
                    "price_brutto": self._format_number(number=item["price"]),
                    "subtotal_brutto": self._format_number(
                        number=item["price"] * item["quantity"]
                    ),
                }
                for item in self.items
            ],
            "total_netto": self._format_price(
                price=self._calc_net_price(price=self.payment["amount"])
            ),
            "total_vat": self._format_price(
                price=self._calc_vat(price=self.payment["amount"])
            ),
            "total_brutto": self._format_price(price=self.payment["amount"]),
            "payment_method": self.payment["method"],
            "payment_status": self.payment["status"],
            "payment_account": self.payment["account"],
            "notes": self.notes,
        }

        os.makedirs(self.INVOICE_DIR, mode=0o777, exist_ok=True)

    def get_invoice_number(self, id: int):
        return "LOOPINV{:07d}".format(id)

    def group_items(self, items):
        grouped = defaultdict(lambda: {"id": "", "name": "", "price": 0, "quantity": 0})

        for item in items:
            key = (item["name"], item["price"])
            if key not in grouped:
                grouped[key] = {
                    "id": item["id"],
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": 0,
                }
            grouped[key]["quantity"] += 1

        return list(grouped.values())

    def _format_id(self, id: int):
        return "{:07d}".format(id)

    def _calc_net_price(self, price: float):
        return float(price) * (1 - self.vat_rate / 100)

    def _calc_net_subtotal(self, price: float, quantity: int):
        return self._calc_net_price(price=price) * quantity

    def _calc_vat(self, price: float):
        return float(price) * (self.vat_rate / 100)

    def _format_number(self, number: float):
        return f"{float(number):,.2f}"

    def _format_price(self, price: float):
        currency = self.payment["currency"]
        return f"{float(price):,.2f} {currency}"

    def _calc_sales(self):
        current_year = datetime.now().year
        previous_year = current_year - 1
        start_date = date(previous_year, 1, 1)
        end_date = date(previous_year, 12, 31)
        sales = Payment.objects.filter(
            status="S", created_at__date__range=(start_date, end_date)
        )
        total_sales = (
            sales.aggregate(total=Sum("amount"))["total"] / 1000
            if sales.count() > 0
            else 0
        )
        return total_sales

    def _is_vat(self):
        return self._calc_sales() > VAT_LIMIT

    def create(self):
        html_content = render_to_string(
            "invoice.html",
            {
                **self.data,
                **{
                    "company": "loop",
                },
            },
        )

        HTML(string=html_content, base_url=FRONTEND_URL).write_pdf(
            self.path, presentational_hints=True
        )

        return self.path

    def _upload(self, storage, location):  # pragma: no cover
        if IS_LOCAL:
            logger.warning("Invoice upload has been skipped", exc_info=True)
            return None

        with open(self.path, "rb") as f:
            return storage.save(location, f)

    def upload(self):
        bucket_name = datetime.today().strftime("%Y%m%d")
        invoices_storage_config = STORAGES.get(
            "invoices",
            {
                "BACKEND": "storages.backends.s3.S3Storage",
                "OPTIONS": {},
            },
        )
        storage_class = get_storage_class(invoices_storage_config["BACKEND"])
        storage = storage_class(**invoices_storage_config["OPTIONS"])
        location = f"{bucket_name}/{self.filename}"

        file_path = self._upload(storage=storage, location=location)

        return storage.url(file_path) if file_path else None

    def remove(self):
        os.remove(self.path)
