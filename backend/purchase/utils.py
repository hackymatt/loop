from typing import List
from django.db.models import Sum
from django.template.loader import render_to_string
from datetime import date, datetime
from purchase.models import Payment
from config_global import VAT_RATE, VAT_LIMIT, FRONTEND_URL
from weasyprint import HTML
import os


class Invoice:
    def __init__(self, customer, items, payment):
        self.PRODUCT_TYPE = "szt."
        self.PRODUCT_QUANTITY = 1
        self.INVOICE_DIR = "invoices"
        self.items = items
        self.payment = payment
        self.date = date.today()
        self.is_vat = self._is_vat()
        self.vat_rate = VAT_RATE if self.is_vat else 0
        self.invoice_number = self._get_invoice_number(self.payment["id"])
        self.customer = customer
        self.path = os.path.join(self.INVOICE_DIR, f"{self.invoice_number}.pdf")

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
                    "quantity": self.PRODUCT_QUANTITY,
                    "price_netto": self._format_price(
                        price=self._calc_net_price(price=item["price"])
                    ),
                    "subtotal_netto": self._format_price(
                        price=self._calc_net_subtotal(
                            price=item["price"], quantity=self.PRODUCT_QUANTITY
                        )
                    ),
                    "vat_percent": f"{self.vat_rate}%",
                    "vat": self._format_price(
                        price=self._calc_vat(price=item["price"])
                    ),
                    "price_brutto": self._format_price(price=item["price"]),
                    "subtotal_brutto": self._format_price(
                        price=item["price"] * self.PRODUCT_QUANTITY
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
        }

        os.makedirs(self.INVOICE_DIR, mode=0o777, exist_ok=True)

    def _get_invoice_number(self, id: int):
        return "LOOPINV{:07d}".format(id)

    def _format_id(self, id: int):
        return "{:07d}".format(id)

    def _calc_net_price(self, price: float):
        return float(price) * (1 - self.vat_rate / 100)

    def _calc_net_subtotal(self, price: float, quantity: int):
        return self._calc_net_price(price=price) * quantity

    def _calc_vat(self, price: float):
        return float(price) * (self.vat_rate / 100)

    def _format_price(self, price: float):
        return "{:,.2f} zł".format(price)

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
                    "website_url": FRONTEND_URL,
                    "company": "loop",
                },
            },
        )

        HTML(string=html_content).write_pdf(self.path)

        return self.path

    def remove(self):
        os.remove(self.path)
