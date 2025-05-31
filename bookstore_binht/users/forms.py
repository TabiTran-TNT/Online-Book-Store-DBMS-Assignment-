from django.contrib.auth import forms as admin_forms
from django.forms import (
    CharField,
    EmailField,
    ModelForm,
    PasswordInput,
)
from django.utils.translation import gettext_lazy as _

from .models import User

PASSWORD_MISMATCH_ERROR = _("New password and confirm password do not match.")


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    # type: ignore[name-defined]
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserUpdateForm(ModelForm):
    current_password = CharField(
        label="Password",
        widget=PasswordInput(
            attrs={
                "placeholder": "Current password",
            },
        ),
        required=False,
    )
    password = CharField(
        label="New Password",
        widget=PasswordInput(
            attrs={
                "placeholder": "New password",
            },
        ),
        required=False,
    )
    confirm_password = CharField(
        label="Confirm Password",
        widget=PasswordInput(
            attrs={
                "placeholder": "Confirm new password",
            },
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "name",
            "current_password",
            "password",
            "confirm_password",
            "email",
            "phone",
            "birthday",
        ]
        labels = {
            "name": "Full Name",
            "email": "Email",
            "phone": "Phone",
            "birthday": "Birthday",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control border-0 rounded-0 ps-2",
                    "readonly": "readonly",
                },
            )
            if field_name in ["current_password", "password", "confirm_password"]:
                field.widget.attrs["class"] += " d-none mb-2"
            else:
                field.required = True

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")

        if current_password and not self.instance.check_password(current_password):
            self.add_error("current_password", _("Current password is incorrect."))

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            self.add_error("confirm_password", PASSWORD_MISMATCH_ERROR)

        return cleaned_data

    def save(self, *, commit=True):
        user = super().save(commit=False)

        current_user = User.objects.get(pk=user.pk)

        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)
        else:
            user.password = current_user.password

        if commit:
            user.save()
        return user
