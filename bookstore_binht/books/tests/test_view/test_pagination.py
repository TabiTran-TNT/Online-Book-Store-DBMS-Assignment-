from django.test import TestCase
from django.urls import reverse

from bookstore_binht.books.tests.factories import BookFactory

HTTP_OK = 200
HTTP_NOT_FOUND = 404
DEFAULT_PAGE_SIZE = 10
CUSTOM_PAGE_SIZE = 5
LAST_DEFAULT_PAGE_SIZE = 5


class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BookFactory.create_batch(25)

    def default_pagination(self):
        response = self.client.get(reverse("home"))
        assert response.status_code == HTTP_OK
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["books"]) == DEFAULT_PAGE_SIZE

    def test_list_all_books(self):
        response = self.client.get(reverse("home") + "?page=3")
        assert len(response.context["books"]) == LAST_DEFAULT_PAGE_SIZE

    def test_elided_page_range(self):
        response = self.client.get(reverse("home"))
        assert response.status_code == HTTP_OK
        assert "elided_page_range" in response.context

    def test_custom_paginate_by(self):
        response = self.client.get(reverse("home") + "?per_page=5")
        assert response.status_code == HTTP_OK
        assert len(response.context["books"]) == CUSTOM_PAGE_SIZE

    def test_invalid_page(self):
        response = self.client.get(reverse("home") + "?page=999")
        assert response.status_code == HTTP_NOT_FOUND
