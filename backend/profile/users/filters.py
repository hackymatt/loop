from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
    BooleanFilter,
)
from profile.models import Profile
from utils.ordering.ordering import OrderFilter


class UserOrderFilter(OrderFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if any(
                field in value
                for field in ["first_name", "last_name", "email", "active"]
            ):
                desc = value[0] == "-"
                modified_value = value[1:] if desc else value
                modified_value = modified_value.replace(
                    modified_value, f"user__{modified_value}"
                )
                modified_value = f"-{modified_value}" if desc else modified_value
                modified_value = modified_value.replace("active", "is_active")
                queryset = queryset.order_by(modified_value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class UserFilter(FilterSet):
    first_name = CharFilter(
        field_name="user__first_name",
        lookup_expr="icontains",
        label="First name zawiera",
    )
    last_name = CharFilter(
        field_name="user__last_name", lookup_expr="icontains", label="Last name zawiera"
    )
    email = CharFilter(
        field_name="user__email", lookup_expr="icontains", label="Email zawiera"
    )
    active = BooleanFilter(field_name="user__is_active", lookup_expr="exact")
    gender = CharFilter(field_name="gender", lookup_expr="icontains")
    user_type = CharFilter(field_name="user_type", lookup_expr="icontains")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    phone_number = CharFilter(field_name="phone_number", lookup_expr="icontains")
    dob = CharFilter(field_name="dob", lookup_expr="icontains")
    street_address = CharFilter(field_name="street_address", lookup_expr="icontains")
    zip_code = CharFilter(field_name="zip_code", lookup_expr="icontains")
    city = CharFilter(field_name="city", lookup_expr="icontains")
    country = CharFilter(field_name="country", lookup_expr="icontains")

    sort_by = UserOrderFilter(
        choices=(
            ("first_name", "First Name ASC"),
            ("-first_name", "First Name DESC"),
            ("last_name", "Last Name ASC"),
            ("-last_name", "Last Name DESC"),
            ("email", "Email ASC"),
            ("-email", "Email DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
            ("gender", "Gender ASC"),
            ("-gender", "Gender DESC"),
            ("user_type", "User Type ASC"),
            ("-user_type", "User Type DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
            ("phone_number", "Phone No ASC"),
            ("-phone_number", "Phone No DESC"),
            ("dob", "DOB ASC"),
            ("-dob", "DOB DESC"),
            ("street_address", "Street Address ASC"),
            ("-street_address", "Street Address DESC"),
            ("zip_code", "Zip Code ASC"),
            ("-zip_code", "Zip Code DESC"),
            ("city", "City ASC"),
            ("-city", "City DESC"),
            ("country", "Country ASC"),
            ("-country", "Country DESC"),
        ),
        fields={
            "first_name": "user__first_name",
            "-first_name": "-user__first_name",
            "last_name": "user__last_name",
            "-last_name": "-user__last_name",
            "email": "user__email",
            "-email": "-user__email",
            "active": "user__is_active",
            "-active": "-user__is_active",
            "gender": "gender",
            "-gender": "-gender",
            "user_type": "user_type",
            "-user_type": "-user_type",
            "created_at": "created_at",
            "-created_at": "-created_at",
            "phone_number": "phone_number",
            "-phone_number": "-phone_number",
            "dob": "dob",
            "-dob": "-dob",
            "street_address": "street_address",
            "-street_address": "-street_address",
            "zip_code": "zip_code",
            "-zip_code": "-zip_code",
            "city": "city",
            "-city": "-city",
            "country": "country",
            "-country": "-country",
        },
    )

    class Meta:
        model = Profile
        fields = ("sort_by",)
