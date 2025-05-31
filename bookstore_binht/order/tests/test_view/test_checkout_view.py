import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from bookstore_binht.cart.tests.factories import CartFactory, CartItemFactory
from bookstore_binht.users.tests.factories import UserFactory

User = get_user_model()

HTTP_OK = 200
HTTP_REDIRECT = 302


@pytest.mark.django_db()
class TestCheckoutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.cart = CartFactory(user=self.user)
        self.cart_item = CartItemFactory(cart=self.cart)
        self.client.force_login(self.user)

    def test_checkout_view_post_valid_form(self):
        # Prepare form data
        form_data = {
            "shipping_address": "123 Test St",
            "zip_code": "12345",
            "city": "Test City",
            "country": "Test Country",
        }

        response = self.client.post(reverse("order:checkout"), data=form_data)
        assert response.status_code == HTTP_REDIRECT
        self.assertRedirects(response, reverse("order:order_payment"))

        session = self.client.session
        assert "checkout_data" in session
        assert session["checkout_data"]["shipping_address"] == "123 Test St"
        assert session["checkout_data"]["zip_code"] == "12345"
        assert session["checkout_data"]["city"] == "Test City"
        assert session["checkout_data"]["country"] == "Test Country"
        assert session["checkout_data"]["full_name"] == self.user.name
        assert session["checkout_data"]["phone"] == self.user.phone

    def test_get_queryset(self):
        response = self.client.get(reverse("order:checkout"))
        assert response.status_code == HTTP_OK

        view = response.wsgi_request.resolver_match.func.view_class()
        view.request = response.wsgi_request

        queryset = view.get_queryset()
        assert list(queryset) == list(self.cart.items.all())

    def test_get_context_data(self):
        response = self.client.get(reverse("order:checkout"))
        assert response.status_code == HTTP_OK

        # Check context data
        context = response.context
        assert "total_price" in context
        assert context["total_price"] == self.cart.get_total_price()

    def test_get_form_kwargs(self):
        response = self.client.get(reverse("order:checkout"))
        assert response.status_code == HTTP_OK

        # Access the view instance
        view = response.wsgi_request.resolver_match.func.view_class()
        view.request = response.wsgi_request

        # Call get_form_kwargs method
        form_kwargs = view.get_form_kwargs()
        assert form_kwargs["user"] == self.user
