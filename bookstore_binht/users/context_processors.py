from django.conf import settings

from bookstore_binht.authentication.forms import UserLoginForm, UserSignupForm
from bookstore_binht.books.models import Category


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def login_form(request):
    return {
        "login_form": UserLoginForm(),
        "signup_form": UserSignupForm(),
    }


def all_categories(request):
    """Return all categories."""
    return {
        "categories": Category.objects.all().order_by("sort_order", "name"),
    }
