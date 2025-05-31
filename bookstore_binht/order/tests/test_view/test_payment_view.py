import os
from unittest.mock import patch

import pytest
import stripe
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from bookstore_binht.cart.models import CartItem
from bookstore_binht.cart.tests.factories import CartFactory, CartItemFactory
from bookstore_binht.order.models import Order, OrderItem
from bookstore_binht.users.tests.factories import UserFactory

User = get_user_model()

HTTP_OK = 200
HTTP_REDIRECT = 302


@pytest.mark.django_db()
class TestOrderPaymentView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.cart = CartFactory(user=self.user)
        self.cart_item = CartItemFactory(cart=self.cart)
        self.client.force_login(self.user)
        session = self.client.session
        session["checkout_data"] = {
            "shipping_address": "123 Test St",
            "zip_code": "12345",
            "city": "Test City",
            "country": "Test Country",
            "full_name": self.user.name,
            "phone": self.user.phone,
        }
        session.save()

    @patch("stripe.PaymentIntent.create")
    @patch("stripe.PaymentIntent.retrieve")
    def test_get_context_data(self, mock_retrieve_intent, mock_create_intent):
        mock_create_intent.return_value = stripe.PaymentIntent.construct_from(
            {
                "id": "pi_123456789",
                "client_secret": "cs_test_123456789",
            },
            "api_key",
        )

        response = self.client.get(reverse("order:order_payment"))
        assert response.status_code == HTTP_OK
        self.assertTemplateUsed(response, "order/payment.html")

        context = response.context
        assert "checkout_data" in context
        assert "cart_items" in context
        assert "total_price" in context
        assert "stripe_publishable_key" in context
        assert "domain" in context
        assert "client_secret" in context

        assert context["checkout_data"] == {
            "shipping_address": "123 Test St",
            "zip_code": "12345",
            "city": "Test City",
            "country": "Test Country",
            "full_name": self.user.name,
            "phone": self.user.phone,
        }
        assert list(context["cart_items"]) == list(self.cart.items.all())
        assert context["total_price"] == self.cart.get_total_price()
        assert context["client_secret"] == os.getenv(
            "CLIENT_SECRET",
            "cs_test_123456789",
        )


@pytest.mark.django_db()
class TestPaymentStatusView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.force_login(self.user)

    @patch("stripe.PaymentIntent.retrieve")
    def test_payment_status_succeeded(self, mock_retrieve_intent):
        mock_retrieve_intent.return_value = stripe.PaymentIntent.construct_from(
            {
                "status": "succeeded",
            },
            "api_key",
        )

        session = self.client.session
        session["checkout_data"] = {
            "shipping_address": "123 Test St",
            "zip_code": "12345",
            "city": "Test City",
            "country": "Test Country",
            "full_name": self.user.name,
            "phone": self.user.phone,
        }
        session.save()

        response = self.client.get(
            reverse("order:payment_status"),
            {"payment_intent": "pi_123456789"},
        )
        assert response.status_code == HTTP_OK
        self.assertTemplateUsed(response, "order/payment_status.html")

        context = response.context
        assert context["status"] == "succeeded"
        assert Order.objects.filter(user=self.user).count() == 1

    @patch("stripe.PaymentIntent.retrieve")
    def test_payment_status_unknown(self, mock_retrieve_intent):
        mock_retrieve_intent.return_value = stripe.PaymentIntent.construct_from(
            {
                "status": "unknown",
            },
            "api_key",
        )

        response = self.client.get(
            reverse("order:payment_status"),
            {"payment_intent": "pi_123456789"},
        )
        assert response.status_code == HTTP_OK
        self.assertTemplateUsed(response, "order/payment_status.html")

        context = response.context
        assert context["status"] == "unknown"
        assert Order.objects.filter(user=self.user).count() == 0


@pytest.mark.django_db()
class TestCashPaymentView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.cart = CartFactory(user=self.user)
        self.cart_item = CartItemFactory(cart=self.cart)
        self.client.force_login(self.user)
        session = self.client.session
        session["checkout_data"] = {
            "shipping_address": "123 Test St",
            "zip_code": "12345",
            "city": "Test City",
            "country": "Test Country",
            "full_name": self.user.name,
            "phone": self.user.phone,
        }
        session.save()

    def test_cash_payment_post(self):
        response = self.client.post(reverse("order:cash_payment"))
        assert response.status_code == HTTP_OK
        self.assertTemplateUsed(response, "order/payment_status.html")

        context = response.context
        assert context["status"] == "succeeded"
        assert Order.objects.filter(user=self.user).count() == 1
        assert OrderItem.objects.filter(order__user=self.user).count() == 1
        assert CartItem.objects.filter(cart=self.cart).count() == 0
        assert "checkout_data" not in self.client.session
