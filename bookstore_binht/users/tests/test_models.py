import datetime
from contextlib import suppress

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils import timezone

from bookstore_binht.users.models import User, validate_not_future_date


def test_validate_not_future_date():
    unexpected_err = "validate_not_future_date raised ValidationError unexpectedly"
    with pytest.raises(ValidationError):
        validate_not_future_date(timezone.now().date() + datetime.timedelta(days=1))

    try:
        validate_not_future_date(timezone.now().date())
    except ValidationError:
        pytest.fail(unexpected_err)

    past_date = timezone.now().date() - datetime.timedelta(days=1)
    try:
        validate_not_future_date(past_date)
    except ValidationError:
        pytest.fail(unexpected_err)


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == reverse("users:update")


def test_invalid_phone_number(user: User, user_password):
    invalid_phone_user = User(
        email="test@example.com",
        phone="012345678",
        birthday=datetime.date(2000, 1, 1),
        name="Test User",
        password=user_password,
    )
    with pytest.raises(ValidationError):
        invalid_phone_user.full_clean()

    invalid_phone_user.phone = "01234567890"
    with pytest.raises(ValidationError):
        invalid_phone_user.full_clean()


def test_invalid_email(user: User, user_password):
    invalid_birthday_user = User(
        name="Test User",
        email="test@example",
        phone="0123456789",
        birthday=datetime.date(2000, 1, 1),
        password=user_password,
    )
    with pytest.raises(ValidationError):
        invalid_birthday_user.full_clean()


def test_invalid_birthday(user: User, user_password):
    invalid_birthday_user = User(
        email="test@example.com",
        phone="0123456789",
        birthday=timezone.now().date() + datetime.timedelta(days=1),
        name="Test User",
        password=user_password,
    )
    with pytest.raises(ValidationError):
        invalid_birthday_user.full_clean()


def test_valid_information(user: User, user_password):
    valid_phone_user = User(
        name="Test User",
        email="test@example.com",
        phone="0123456789",
        birthday=datetime.date(2000, 1, 1),
        password=user_password,
    )
    try:
        valid_phone_user.full_clean()
        valid_phone_user.save()
    except ValidationError:
        pytest.fail(
            "User with valid phone number raised"
            " ValidationError unexpectedly: {e.message}",
        )


def test_duplicate_email(user: User, user_password):
    valid_phone_user = User(
        name="Test User",
        email="test@example.com",
        phone="0123456789",
        birthday=datetime.date(2000, 1, 1),
        password=user_password,
    )
    valid_phone_user.save()

    duplicate_email_user = User(
        name="Test User",
        email="test@example.com",
        phone="0123456798",
        birthday=datetime.date(2000, 1, 1),
        password=user_password,
    )
    with suppress(IntegrityError):
        duplicate_email_user.save()
        pytest.fail("User with duplicate email saved unexpectedly.")
