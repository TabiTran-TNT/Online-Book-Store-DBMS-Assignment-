import datetime

from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.utils import user_email, user_username
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import CharField, EmailField, IntegerField, TextInput
from django.utils.translation import gettext_lazy as _

from bookstore_binht.users.models import validate_not_future_date

MIN_BIRTH_YEAR = 1900
MAX_DAYS_IN_MONTH = 31
MONTHS_IN_YEAR = 12


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    email = EmailField(
        label=_("Email address"),
        label_suffix="",
        widget=TextInput(
            attrs={
                "type": "email",
                "autocomplete": "email",
                "class": "form-control",
            },
        ),
    )

    phone = CharField(
        label=_("Phone no."),
        widget=TextInput(
            attrs={
                "autocomplete": "tel",
                "class": "form-control",
            },
        ),
        required=True,
        validators=[
            RegexValidator(
                regex=r"^(0\d{9}|(\+\d{1,3})\d{9})$",
                message=_(
                    "Invalid phone number.",
                ),
            ),
        ],
    )

    name = CharField(
        label_suffix="",
        label=_("Full name"),
        widget=TextInput(
            attrs={
                "autocomplete": "name",
                "class": "form-control",
            },
        ),
        required=True,
    )

    birth_day = IntegerField(
        label_suffix="",
        label=_("Day"),
        widget=TextInput(
            attrs={
                "class": "form-control",
            },
        ),
        required=True,
    )

    birth_month = IntegerField(
        label_suffix="",
        label=_("Month"),
        widget=TextInput(
            attrs={
                "class": "form-control",
            },
        ),
        required=True,
    )

    birth_year = IntegerField(
        label_suffix="",
        label=_("Year"),
        widget=TextInput(
            attrs={
                "class": "form-control",
            },
        ),
        required=True,
    )

    field_order = [
        "email",
        "password1",
        "password2",
        "phone",
        "name",
        "birth_day",
        "birth_month",
        "birth_year",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            field[1].widget.attrs.update({"class": "form-control"})

        self.fields["password1"].label_suffix = ""

        if "password2" in self.fields:
            self.fields["password2"].label_suffix = ""

    def clean(self):
        super().clean()
        self.cleaned_data = self._clean_password()
        self._clean_birthday()
        return self.cleaned_data

    def _clean_password(self):
        user = get_user_model()
        dummy_user = user()
        user_username(dummy_user, self.cleaned_data.get("username"))
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password1")

        if password:
            self._validate_password(password, dummy_user)

        self._check_password_match()

        return self.cleaned_data

    def _validate_password(self, password, dummy_user):
        try:
            get_adapter().clean_password(password, user=dummy_user)
        except ValidationError as e:
            self.add_error("password1", e)

    def _check_password_match(self):
        if (
            app_settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("You must type the same password each time."),
                )

    def _clean_birthday(self):
        birth_day = self.cleaned_data.get("birth_day")
        birth_month = self.cleaned_data.get("birth_month")
        birth_year = self.cleaned_data.get("birth_year")

        self._validate_birth_date(birth_day, birth_month, birth_year)

        if all([birth_day, birth_month, birth_year]):
            self._set_birthday(birth_day, birth_month, birth_year)

    def _validate_birth_date(self, day, month, year):
        if not (1 <= day <= MAX_DAYS_IN_MONTH):
            self.add_error("birth_day", _("Invalid date."))
        if not (1 <= month <= MONTHS_IN_YEAR):
            self.add_error("birth_month", _("Invalid date."))
        if not (
            MIN_BIRTH_YEAR <= year <= datetime.datetime.now(tz=datetime.UTC).date().year
        ):
            self.add_error("birth_year", _("Invalid date."))

    def _set_birthday(self, day, month, year):
        try:
            birthday = datetime.date(year, month, day)
            validate_not_future_date(birthday)
            self.cleaned_data["birthday"] = birthday
        except ValueError:
            self.add_error("birth_year", _("Invalid date."))
        except ValidationError as e:
            self.add_error("birth_day", e)

    def custom_signup(self, request, user):
        user.phone = self.cleaned_data["phone"]
        user.birthday = self.cleaned_data["birthday"]
        user.name = self.cleaned_data["name"]
        user.email = self.cleaned_data["email"]
        user.save()


MAX_LOGIN_ATTEMPTS = 3


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request", None)
        super().__init__(*args, **kwargs)

        if (
            self.request
            and self.request.session.get("login_attempts", 0) >= MAX_LOGIN_ATTEMPTS
        ):
            self.fields["captcha"] = CaptchaField()

        for field_name, field in self.fields.items():
            if field_name == "remember":
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

        self.fields["password"].label_suffix = ""

    def clean(self):
        cleaned_data = super().clean()
        if "captcha" in self.fields:
            self.cleaned_data.get("captcha")
        return cleaned_data
