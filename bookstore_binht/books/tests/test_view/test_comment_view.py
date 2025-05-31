import os
from decimal import Decimal

import pytest
from django.contrib import messages
from django.urls import reverse

from bookstore_binht.books.forms import CommentForm
from bookstore_binht.books.models import Book, Comment
from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.users.models import User

HTTP_OK = 200
HTTP_NOT_FOUND = 404
TOTAL_BOOKS = 2
TOTAL_CATEGORIES = 2
SINGLE_BOOK = 1
INVALID_CATEGORY_ID = 999
NUM_COMMENT = 5


@pytest.mark.django_db()
class TestBookCommentListView:
    def setup_method(self, method):
        password = os.environ.get("DJANGO_USER", "12345")
        self.user = [
            User.objects.create_user(
                email=f"testuse{i}@example.com",
                password=password,
                name=f"Test User {i}",
                phone="0123456789",
                birthday="1990-01-01",
            )
            for i in range(6)
        ]
        BookFactory(
            title="Test Book",
            author_name="Test Author",
            publisher_name="Test Publisher",
            unit_price=Decimal("9.99"),
            description="Test description",
        ).save()
        self.book = Book.objects.first()
        self.comments = [
            Comment.objects.create(
                book=self.book,
                author=self.user[i],
                content=f"Test comment {i}",
                rating=5,
            )
            for i in range(5)
        ]

    def test_view_url_exists_at_desired_location(self, client):
        response = client.get(f"/books/{self.book.id}/comment/")
        assert response.status_code == HTTP_OK

    def test_view_url_accessible_by_name(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK
        assert "books/book_comments.html" in [t.name for t in response.templates]

    def test_lists_all_comments(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK
        assert len(response.context["comments"]) == NUM_COMMENT

    def test_book_in_context(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK
        assert "book" in response.context
        assert response.context["book"] == self.book

    def test_comments_ordered_by_created_descending(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK
        assert list(response.context["comments"]) == list(
            Comment.objects.filter(book=self.book).order_by("-created"),
        )

    def test_view_returns_404_for_invalid_book_id(self, client):
        response = client.get(reverse("books:book_comments", args=[999]))
        assert response.status_code == HTTP_NOT_FOUND

    def test_no_comments(self, client):
        Comment.objects.all().delete()
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK
        assert len(response.context["comments"]) == 0

    def test_context_data(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert response.status_code == HTTP_OK
        assert "comments" in response.context
        assert "book" in response.context
        assert response.context["book"] == self.book
        assert len(response.context["comments"]) == NUM_COMMENT

    def test_form_in_context(self, client):
        response = client.get(reverse("books:book_comments", args=[self.book.id]))
        assert "form" in response.context
        assert isinstance(response.context["form"], CommentForm)

    def test_post_comment_logged_in(self, client):
        user = User.objects.get(email="testuse5@example.com")
        client.force_login(user)
        comment_data = {"content": "New comment", "rating": 4, "user": user}
        response = client.post(
            reverse("books:book_comments", args=[self.book.id]),
            comment_data,
            follow=True,
        )
        assert response.status_code == HTTP_OK
        assert Comment.objects.filter(book=self.book).count() == NUM_COMMENT + 1

    def test_post_comment_not_logged_in(self, client):
        comment_data = {"content": "New comment", "rating": 4}
        response = client.post(
            reverse("books:book_comments", args=[self.book.id]),
            comment_data,
        )
        messages_list = list(messages.get_messages(response.wsgi_request))
        assert len(messages_list) == 1
        assert str(messages_list[0]) == "You need to be logged in to post a comment."
