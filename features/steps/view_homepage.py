from decimal import Decimal

from behave import given, then, when
from django.utils import timezone
from selenium.webdriver.common.by import By

from bookstore_binht.books.models import Book
from bookstore_binht.books.tests.factories import BookFactory


@when('I visit "/"')
def visit_homepage(context):
    context.browser.get(context.get_url("/"))


@then("I should see the navbar with the link to home")
def check_navbar(context):
    navbar = context.browser.find_element(By.CSS_SELECTOR, ".navbar")
    assert navbar.is_displayed()


@given("there are books in the database")
def add_books_to_db(context):
    BookFactory(
        title="The Great Gatsby",
        description="A novel by F. Scott Fitzgerald",
        author_name="F. Scott Fitzgerald",
        publisher_name="Scribner",
        published_date=timezone.now().date(),
        unit_price=Decimal("15.99"),
        photo="/media/Book_1.png",
        total_rating_value=45,
        total_rating_count=10,
    ).save()

    BookFactory(
        title="To Kill a Mockingbird",
        description="A novel by Harper Lee",
        author_name="Harper Lee",
        publisher_name="J. B. Lippincott & Co.",
        published_date=timezone.now().date(),
        unit_price=Decimal("12.99"),
        photo="/media/Book_2.png",
        total_rating_value=30,
        total_rating_count=6,
    ).save()


@then(
    "I should see a list of books"
    " with their images, titles, authors, unit prices, and ratings",
)
def check_book_info(context):
    book_images = context.browser.find_elements(By.NAME, "book-image")
    book_titles = context.browser.find_elements(By.NAME, "book-title")
    book_authors = context.browser.find_elements(By.NAME, "author-name")
    book_prices = context.browser.find_elements(By.NAME, "button-price")
    book_ratings = context.browser.find_elements(By.NAME, "rating")

    for itr in range(Book.objects.count()):
        assert book_images[itr].is_displayed()
        assert book_titles[itr].is_displayed()
        assert book_authors[itr].is_displayed()
        assert book_prices[itr].is_displayed()
        assert book_ratings[itr].is_displayed()

    assert len(book_images) == Book.objects.count()
    assert len(book_titles) == Book.objects.count()
    assert len(book_authors) == Book.objects.count()
    assert len(book_prices) == Book.objects.count()
    assert len(book_ratings) == Book.objects.count()
