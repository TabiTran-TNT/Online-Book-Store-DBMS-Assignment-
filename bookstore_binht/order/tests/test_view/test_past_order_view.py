import pytest
from django.test import Client, TestCase
from django.urls import reverse

from bookstore_binht.order.tests.factories import (
    OrderItemFactory,
    OrderModelFactory,
)
from bookstore_binht.users.tests.factories import UserFactory

HTTP_OK = 200
NUM_HISTORY_ORDERS = 2


@pytest.mark.django_db()
class TestPastOrderListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.force_login(self.user)
        self.order1 = OrderModelFactory(user=self.user)
        self.order2 = OrderModelFactory(user=self.user)
        OrderItemFactory(order=self.order1)
        OrderItemFactory(order=self.order2)

    def test_get_past_orders(self):
        response = self.client.get(reverse("order:order_history"))
        assert response.status_code == HTTP_OK
        self.assertTemplateUsed(response, "order/past_order_list.html")

        context = response.context
        assert "orders" in context
        orders = context["orders"]
        assert orders.count() == NUM_HISTORY_ORDERS
        assert orders[0] == self.order2
        assert orders[1] == self.order1
