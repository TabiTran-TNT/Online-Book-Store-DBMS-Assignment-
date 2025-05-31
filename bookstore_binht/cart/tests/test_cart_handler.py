from decimal import Decimal

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import Client

from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.cart.cart import CartHandler
from bookstore_binht.cart.models import CartItem
from bookstore_binht.users.tests.factories import UserFactory

MERGE_CART_ITEM = 2


@pytest.mark.django_db()
class TestCartHandler:
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.book = BookFactory(unit_price=200000.00)
        self.book2 = BookFactory(unit_price=300000.00)
        self.session = self.client.session

    def test_add_item_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)

        cart_item = CartItem.objects.get(cart=self.user.cart, book=self.book)
        assert cart_item.quantity == 1

    def test_add_item_unauthenticated_user(self):
        request = self.client.get("/")

        request.session = self.session
        request.user = AnonymousUser()

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)

        assert str(self.book.id) in request.session[settings.CART_SESSION_ID]
        assert (
            request.session[settings.CART_SESSION_ID][str(self.book.id)]["quantity"]
            == 1
        )

    def test_decrease_item_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.decrease(self.book)

        assert CartItem.objects.filter(cart=self.user.cart, book=self.book).count() == 0

    def test_decrease_item_unauthenticated_user(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.decrease(self.book)

        assert str(self.book.id) not in request.session[settings.CART_SESSION_ID]

    def test_remove_item_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.remove(self.book)

        assert CartItem.objects.filter(cart=self.user.cart, book=self.book).count() == 0

    def test_remove_item_unauthenticated_user(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.remove(self.book)

        assert str(self.book.id) not in request.session[settings.CART_SESSION_ID]

    def test_get_total_price_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.add(self.book2)

        total_price = cart_handler.get_total_price()
        assert total_price == "500,000đ"

    def test_get_total_price_unauthenticated_user(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.add(self.book2)

        total_price = cart_handler.get_total_price()
        assert total_price == "500,000đ"

    def test_clear_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.clear()

        assert CartItem.objects.filter(cart=self.user.cart).count() == 0

    def test_clear_unauthenticated_user(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.clear()

        assert settings.CART_SESSION_ID not in request.session

    def test_merge_cart_to_db(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)
        cart_handler.add(self.book2)

        self.client.force_login(self.user)
        request.user = self.user
        cart_handler = CartHandler(request)
        cart_handler.merge_cart_to_db()

        cart_items = CartItem.objects.filter(cart=self.user.cart)
        assert cart_items.count() == MERGE_CART_ITEM
        assert cart_items.get(book=self.book).quantity == 1
        assert cart_items.get(book=self.book2).quantity == 1

    def test_save(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.save()
        assert request.session.modified

    def test_iter_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)

        items = list(cart_handler)
        assert len(items) == 1
        assert items[0]["book"] == self.book
        assert items[0]["quantity"] == 1
        assert items[0]["price"] == self.book.unit_price

    def test_iter_unauthenticated_user(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)

        items = list(cart_handler)
        assert len(items) == 1
        assert items[0]["book"] == self.book
        assert items[0]["quantity"] == 1
        assert items[0]["price"] == Decimal(self.book.unit_price)

    def test_len_authenticated_user(self):
        self.client.force_login(self.user)
        request = self.client.get("/")
        request.user = self.user
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)

        assert len(cart_handler) == 1

    def test_len_unauthenticated_user(self):
        request = self.client.get("/")
        request.user = AnonymousUser()
        request.session = self.session

        cart_handler = CartHandler(request)
        cart_handler.add(self.book)

        assert len(cart_handler) == 1
