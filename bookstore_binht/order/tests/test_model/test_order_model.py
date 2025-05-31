from django.contrib.auth import get_user_model
from django.test import TestCase

from bookstore_binht.order.tests.factories import OrderItemFactory, OrderModelFactory
from bookstore_binht.users.tests.factories import UserFactory

User = get_user_model()

SHIPPING_ADDRESS = "123 Test St"
ZIP_CODE = "12345"
CITY = "Test City"
COUNTRY = "Test Country"
UNIT_PRICE_1 = 10.0
UNIT_PRICE_2 = 15.0
QUANTITY_1 = 2
QUANTITY_2 = 1
TOTAL_PRICE = 35.00
COST = 20.00


class OrderModelTests(TestCase):
    def test_order_creation(self):
        user = UserFactory()
        order = OrderModelFactory(user=user)
        assert order.user.username == user.username
        assert order.shipping_address == SHIPPING_ADDRESS
        assert order.zip_code == ZIP_CODE
        assert order.city == CITY
        assert order.country == COUNTRY

    def test_order_total_price(self):
        order = OrderModelFactory()
        OrderItemFactory(order=order, unit_price=UNIT_PRICE_1, quantity=QUANTITY_1)
        OrderItemFactory(order=order, unit_price=UNIT_PRICE_2, quantity=QUANTITY_2)
        assert order.get_total_price() == TOTAL_PRICE

    def test_order_str(self):
        order = OrderModelFactory()
        expected_str = f"Order {order.id} - {order.user.username}"
        assert str(order) == expected_str
