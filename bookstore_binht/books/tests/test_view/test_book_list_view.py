from urllib.parse import urlencode

import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from bookstore_binht.books.models import Category
from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.books.views import BookListView

HTTP_OK = 200
HTTP_ERROR = 404
HTTP_NOT_FOUND = 404
TOTAL_BOOKS = 2
TOTAL_CATEGORIES = 2
SINGLE_BOOK = 1
INVALID_CATEGORY_ID = 999
NUM_COMMENT = 5


@pytest.mark.django_db()
class TestBookListView:
    def setup_method(self):
        self.factory = RequestFactory()
        self.category1 = Category.objects.create(name="Fiction", sort_order=1)
        self.category2 = Category.objects.create(name="Non-fiction", sort_order=2)
        self.book1 = BookFactory(
            title="Book 1",
            description="Description 1",
            author_name="Author 1",
            publisher_name="Publisher 1",
            unit_price=10.99,
        )
        self.book1.categories.add(self.category1)
        self.book2 = BookFactory(
            title="Book 2",
            description="Description 2",
            author_name="Author 2",
            publisher_name="Publisher 2",
            unit_price=15.99,
        )
        self.book2.categories.add(self.category2)

    def test_book_list_view_no_category_no_search(self):
        url = reverse("home")
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["books"]) == TOTAL_BOOKS
        assert "categories" in response.context_data
        assert response.context_data["selected_category"] is None
        assert response.context_data["search_query"] == ""

    def test_book_list_view_with_category(self):
        query_params = {"category": self.category1.id}
        url = f"{reverse('home')}?{urlencode(query_params)}"
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["books"]) == SINGLE_BOOK
        assert response.context_data["books"][0] == self.book1
        assert response.context_data["selected_category"] == self.category1.id

    def test_book_list_view_invalid_category(self):
        query_params = {"category": INVALID_CATEGORY_ID}
        url = f"{reverse('home')}?{urlencode(query_params)}"
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["books"]) == 0
        assert response.context_data["selected_category"] == INVALID_CATEGORY_ID

    def test_book_list_view_with_search(self):
        query_params = {"search": "Book 1"}
        url = f"{reverse("home")}?{urlencode(query_params)}"
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["books"]) == SINGLE_BOOK
        assert response.context_data["books"][0] == self.book1
        assert response.context_data["search_query"] == "Book 1"

    def test_book_list_view_with_search_author(self):
        query_params = {"search": "Author 2"}
        url = f"{reverse('home')}?{urlencode(query_params)}"
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["books"]) == SINGLE_BOOK
        assert response.context_data["books"][0] == self.book2
        assert response.context_data["search_query"] == "Author 2"

    def test_book_list_view_with_search_no_results(self):
        query_params = {"search": "Nonexistent"}
        url = f"{reverse('home')}?{urlencode(query_params)}"
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert response.status_code == HTTP_OK
        assert len(response.context_data["books"]) == 0
        assert response.context_data["search_query"] == "Nonexistent"

    def test_categories_in_context(self):
        url = reverse("home")
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        categories = response.context_data["categories"]
        assert len(categories) == TOTAL_CATEGORIES
        assert categories[0] == self.category1
        assert categories[1] == self.category2

    def test_template_used(self):
        url = reverse("home")
        request = self.factory.get(url)
        response = BookListView.as_view()(request)

        assert isinstance(response, HttpResponse)
        assert response.template_name[0] == "home.html"
