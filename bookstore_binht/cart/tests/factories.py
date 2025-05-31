import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.cart.models import Cart, CartItem
from bookstore_binht.users.tests.factories import UserFactory

User = get_user_model()


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    book = factory.SubFactory(BookFactory)
    quantity = factory.Faker("random_int", min=1, max=10)
