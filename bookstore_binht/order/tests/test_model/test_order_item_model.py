from django.contrib.auth import get_user_model
from django.test import TestCase

from bookstore_binht.order.tests.factories import OrderItemFactory

User = get_user_model()

UNIT_PRICE_1 = 10.0
QUANTITY_1 = 2
COST = 20.00


class OrderItemModelTests(TestCase):
    def test_order_item_creation(self):
        order_item = OrderItemFactory()
        assert order_item.unit_price == UNIT_PRICE_1
        assert order_item.quantity == QUANTITY_1
        assert order_item.get_cost() == COST

    def test_order_item_str(self):
        order_item = OrderItemFactory()
        expected_str = (
            f"{QUANTITY_1} of {order_item.book.title} "
            f"in order {order_item.order.id}"
        )
        assert str(order_item) == expected_str
