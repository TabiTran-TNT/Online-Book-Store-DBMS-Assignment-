import factory
from factory.django import DjangoModelFactory

from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.order.models import Order, OrderItem
from bookstore_binht.users.tests.factories import UserFactory


class OrderModelFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    shipping_address = "123 Test St"
    zip_code = "12345"
    city = "Test City"
    country = "Test Country"

    class Meta:
        model = Order


class OrderItemFactory(DjangoModelFactory):
    order = factory.SubFactory(OrderModelFactory)
    book = factory.SubFactory(BookFactory)
    unit_price = 10.00
    quantity = 2

    class Meta:
        model = OrderItem
