import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from bookstore_binht.authentication.views import CustomLoginView, CustomSignupView
from bookstore_binht.users.tests.factories import UserFactory

HTTP_OK = 200
HTTP_ERROR = 400


@pytest.mark.django_db()
class TestCustomLoginView:
    def setup_method(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.url = reverse("account_login")

        def get_response(request):
            return HttpResponse(status=HTTP_OK)

        self.middleware = SessionMiddleware(get_response)
        self.message_middleware = MessageMiddleware(get_response)

        request = self.factory.get("/")

        self.middleware.process_request(request)
        self.message_middleware.process_request(request)

        self.session = request.session

    def setup_request(self, request):
        request.session = self.session
        request.user = AnonymousUser()

        messages_storage = FallbackStorage(request)
        request._messages = messages_storage
        request.session.save()
        return request

    def test_login_attempts_reset_on_success(self):
        request = self.factory.post(
            self.url,
            {"login": "binh.tran0611csbk@hcmut.edu.vn", "password": "06112003"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        request = self.setup_request(request)

        response = CustomLoginView.as_view()(request)

        assert request.session.get("login_attempts") == 0
        assert response.status_code == HTTP_OK
        response_data = json.loads(json.loads(response.content)["html"])

        assert response_data["status"] == 1
        assert "new_cptch_key" in response_data
        assert "new_cptch_image" in response_data

    def test_login_attempts_increment_on_failure(self):
        request = self.factory.post(
            self.url,
            {"login": "test@example.com", "password": "wrongpassword"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        request = self.setup_request(request)

        response = CustomLoginView.as_view()(request)

        assert request.session.get("login_attempts") == 1
        assert response.status_code == HTTP_ERROR
        response_data = json.loads(json.loads(response.content)["html"])

        assert response_data["status"] == 0
        assert "form_errors" in response_data
        assert "new_cptch_key" in response_data
        assert "new_cptch_image" in response_data
        assert "show_captcha" in response_data

    def test_unverified_email_on_login(self):
        email_address = self.user.emailaddress_set.first()
        email_address.verified = False
        email_address.save()

        request = self.factory.post(
            self.url,
            {"login": self.user.email, "password": "06112003"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        request = self.setup_request(request)

        response = CustomLoginView.as_view()(request)

        assert response.status_code == HTTP_OK
        response_data = json.loads(json.loads(response.content)["html"])

        assert response_data["status"] == "unverified"
        assert response_data["email"] == self.user.email


@pytest.mark.django_db()
class TestCustomSignupView:
    def setup_method(self):
        self.factory = RequestFactory()
        self.url = reverse("account_signup")

        def get_response(request):
            return HttpResponse(status=HTTP_OK)

        self.middleware = SessionMiddleware(get_response)
        self.message_middleware = MessageMiddleware(get_response)

        request = self.factory.get("/")

        self.middleware.process_request(request)
        self.message_middleware.process_request(request)

        self.session = request.session

    def setup_request(self, request):
        request.session = self.session
        request.user = AnonymousUser()

        messages_storage = FallbackStorage(request)
        request._messages = messages_storage
        request.session.save()
        return request

    def test_signup_success(self):
        request = self.factory.post(
            self.url,
            {
                "email": "newuser@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
                "phone": "0859007204",
                "name": "New User",
                "birth_day": 6,
                "birth_month": 11,
                "birth_year": 2003,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        request = self.setup_request(request)

        response = CustomSignupView.as_view()(request)

        assert response.status_code == HTTP_OK
        response_data = json.loads(json.loads(response.content)["html"])

        assert response_data["status"] == "success"
        assert "username" in response_data
