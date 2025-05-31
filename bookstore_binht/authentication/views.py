import json

from allauth.account import app_settings as allauth_app_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import complete_signup
from allauth.account.views import LoginView as AllauthLoginView
from allauth.account.views import SignupView as AllauthSignupView
from allauth.core.exceptions import ImmediateHttpResponse
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from bookstore_binht.authentication.forms import UserLoginForm

LIMIT_LOGIN_ATTEMPTS = 3


class CustomLoginView(AllauthLoginView):
    form_class = UserLoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        self.request.session["login_attempts"] = 0
        user = form.user
        email_address = EmailAddress.objects.get(user=user, email=user.email)

        if email_address and not email_address.verified:
            email_address.send_confirmation(self.request)
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {"status": "unverified", "email": user.email},
                    status=200,
                )

        response = super().form_valid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            key = CaptchaStore.generate_key()
            to_json_response = {
                "status": 1,
                "new_cptch_key": key,
                "new_cptch_image": captcha_image_url(key),
            }
            return HttpResponse(
                json.dumps(to_json_response),
                content_type="application/json",
            )
        return response

    def form_invalid(self, form):
        self.request.session["login_attempts"] = (
            self.request.session.get("login_attempts", 0) + 1
        )
        show_captcha = self.request.session["login_attempts"] >= LIMIT_LOGIN_ATTEMPTS
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            key = CaptchaStore.generate_key()
            to_json_response = {
                "status": 0,
                "form_errors": form.errors,
                "new_cptch_key": key,
                "new_cptch_image": captcha_image_url(key),
                "show_captcha": show_captcha,
            }
            return HttpResponse(
                json.dumps(to_json_response),
                content_type="application/json",
            )
        return super().form_invalid(form)


class CustomSignupView(AllauthSignupView):
    @method_decorator(sensitive_post_parameters("password", "password1", "password2"))
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.user, resp = form.try_save(self.request)
        if resp:
            if isinstance(resp, HttpResponseRedirect):
                if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "A user is already registered"
                            " with this email address.",
                        },
                        status=400,
                    )
            return resp
        try:
            redirect_url = self.get_success_url()
            complete_signup(
                self.request,
                self.user,
                email_verification=allauth_app_settings.EMAIL_VERIFICATION,
                success_url=redirect_url,
            )
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {"status": "success", "username": self.user.name},
                    status=200,
                )
            return super().form_valid(form)
        except ImmediateHttpResponse as e:
            return e.response
