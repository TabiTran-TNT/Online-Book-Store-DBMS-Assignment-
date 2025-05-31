from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, DateField, EmailField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .exceptions import FutureDateValidationError
from .managers import UserManager


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise FutureDateValidationError


class User(AbstractUser):
    """
    Default custom user model for Bookstore BinhT.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]
    phone = CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r"^(0\d{9}|(\+\d{1,3})\d{9})$",
                message="Invalid phone number.",
            ),
        ],
        blank=True,
        default="",
    )
    # The birthday date cannot be in the future
    birthday = DateField(blank=True, null=True, validators=[validate_not_future_date])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:update")

    def get_first_name(self) -> str:
        return self.name.split()[0]

    def get_last_name(self) -> str:
        parts = self.name.split()[1:]
        return " ".join(parts)
