import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from bookstore_binht.books.tests.factories import BookFactory, CategoryFactory
from bookstore_binht.cart.cart import CartHandler
from bookstore_binht.cart.views import CartListView, add_to_cart, cart_remove
from bookstore_binht.users.tests.factories import UserFactory

HTTP_OK = 200
HTTP_ERROR = 404
HTTP_REDIRECT = 302
NUMBER_OF_BOOKS = 2


@pytest.mark.django_db()
class TestCart:
    def setup_method(self):
        self.factory = RequestFactory()

        def get_response(request):
            return HttpResponse(status=200)

        self.middleware = SessionMiddleware(get_response)

        request = self.factory.get("/")
        self.middleware.process_request(request)

        self.session = request.session

        self.category = CategoryFactory()
        self.book1 = BookFactory()
        self.book2 = BookFactory()

        self.book1.categories.add(self.category)
        self.book2.categories.add(self.category)

        self.user = UserFactory()

    def setup_request(self, request, user=None):
        self.middleware.process_request(request)
        request.session = self.session
        if user:
            request.user = user
        else:
            request.user = AnonymousUser()
        return request

    def test_add_to_cart_unauthenticated(self):
        url = reverse("cart:add_to_cart")
        request = self.factory.post(url, {"book_id": self.book1.id})
        request = self.setup_request(request)
        response = add_to_cart(request)

        assert response.status_code == HTTP_OK

        cart = CartHandler(request)
        assert len(cart) == 1
        assert cart.cart[str(self.book1.id)]["quantity"] == 1

    def test_remove_from_cart_unauthenticated(self):
        request = self.factory.post("/")
        request = self.setup_request(request)

        cart = CartHandler(request)
        cart.add(self.book1)

        url = reverse("cart:cart_remove", args=[self.book1.id])
        request = self.factory.post(url)
        request = self.setup_request(request)
        response = cart_remove(request, self.book1.id)

        assert response.status_code == HTTP_REDIRECT

        cart = CartHandler(request)
        assert cart.__len__() == 0

    def test_cart_list_view_unauthenticated(self):
        request = self.factory.get("/")
        request = self.setup_request(request)

        cart = CartHandler(request)
        cart.add(self.book1)
        cart.add(self.book2)

        response = CartListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["cart"]) == NUMBER_OF_BOOKS
        assert response.context_data["total_price"] == cart.get_total_price()

    def test_clear_cart_unauthenticated(self):
        request = self.factory.get("/")
        request = self.setup_request(request)

        cart = CartHandler(request)
        cart.add(self.book1)

        cart = CartHandler(request)
        assert cart.__len__() == 1

        cart.clear()
        cart = CartHandler(request)
        assert cart.__len__() == 0

    def test_add_to_cart_authenticated(self):
        url = reverse("cart:add_to_cart")
        request = self.factory.post(url, {"book_id": self.book1.id})
        request = self.setup_request(request, user=self.user)
        response = add_to_cart(request)

        assert response.status_code == HTTP_OK

        cart = CartHandler(request)
        assert len(cart) == 1
        assert cart.cart.items.filter(book=self.book1).count() == 1

    def test_remove_from_cart_authenticated(self):
        url = reverse("cart:add_to_cart")
        request = self.factory.post(url, {"book_id": self.book1.id})
        request = self.setup_request(request, user=self.user)
        add_to_cart(request)

        url = reverse("cart:cart_remove", args=[self.book1.id])
        request = self.factory.post(url)
        request = self.setup_request(request, user=self.user)
        response = cart_remove(request, self.book1.id)

        assert response.status_code == HTTP_REDIRECT

        cart = CartHandler(request)
        assert cart.__len__() == 0

    def test_cart_list_view_authenticated(self):
        request = self.factory.get("/")
        request = self.setup_request(request, user=self.user)

        cart = CartHandler(request)
        cart.add(self.book1)
        cart.add(self.book2)

        response = CartListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["cart"]) == NUMBER_OF_BOOKS
        assert response.context_data["total_price"] == cart.get_total_price()

    def test_clear_cart_authenticated(self):
        request = self.factory.get("/")
        request = self.setup_request(request, user=self.user)

        cart = CartHandler(request)
        cart.add(self.book1)

        cart = CartHandler(request)
        assert cart.__len__() == 1

        cart.clear()
        cart = CartHandler(request)
        assert cart.__len__() == 0
