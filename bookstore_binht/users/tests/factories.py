import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from factory import post_generation
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    email = "binh.tran0611csbk@hcmut.edu.vn"
    name = "Binh Tran"
    phone = "0859007204"
    birthday = datetime.date(2003, 11, 6)

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted if extracted else "06112003"
        self.set_password(password)
        if create:
            self.save()

    @post_generation
    def email_address(self, create, extracted, **kwargs):
        if create:
            email_address, created = EmailAddress.objects.get_or_create(
                user=self,
                email=self.email,
            )
            email_address.verified = True
            email_address.primary = True
            email_address.save()

    class Meta:
        model = User
        django_get_or_create = ["email"]
        skip_postgeneration_save = True
