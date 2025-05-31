from behave import given, then, when
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.models import Book, Comment
from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.users.models import User


@given("the following users exist in the database")
def add_users(context):
    for row in context.table:
        User.objects.create(
            email=row["Email"],
            name=row["Name"],
            phone=row["Phone"],
            birthday=row["Birthday"],
        )


@given("there is a book in the database with the following details")
def add_book(context):
    book_data = context.table[0]
    BookFactory(
        title=book_data["Title"],
        author_name=book_data["Author"],
        publisher_name=book_data["Publisher"],
        published_date=book_data["Published Date"],
        unit_price=book_data["Price"],
    ).save()
    context.book = Book.objects.get(title=book_data["Title"])


@given('the book "{book_title}" has the following comments')
def add_comment(context, book_title):
    book = Book.objects.get(title=book_title)
    for row in context.table:
        user = User.objects.get(email=row["User Email"])
        Comment.objects.create(
            book=book,
            author=user,
            rating=int(row["Rating"]),
            content=row["Content"],
            created=row["Date"],
        )


@given('I am on the book details page for "{book_title}"')
def browse_book_detail(context, book_title):
    book = Book.objects.get(title=book_title)
    context.browser.get(
        context.get_url(reverse("books:book_detail", kwargs={"pk": book.id})),
    )


@given('I am on the comments page for "{book_title}"')
def browse_comment_page(context, book_title):
    book = Book.objects.get(title=book_title)

    comments_url = context.get_url(
        reverse("books:book_comments", kwargs={"pk": book.id}),
    )

    context.browser.get(comments_url)


@when("I click on the link to the rating page")
def click_direct_to_comments(context):
    link = WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "view-comments")),
    )
    link.click()


@then('I should be on the comments page for "{book_title}"')
def check_comment_page_url(context, book_title):
    book = Book.objects.get(title=book_title)
    expected_url = context.get_url(
        reverse("books:book_comments", kwargs={"pk": book.id}),
    )
    WebDriverWait(context.browser, 10).until(
        ec.url_to_be(expected_url),
    )
    assert context.browser.current_url == expected_url


@then('I should see the title "{book_title}"')
def check_book_title(context, book_title):
    title_element = WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "book-title")),
    )
    assert f"{book_title}" in title_element.text


@then("I should see {count:d} comments")
def check_num_comments(context, count):
    comments = WebDriverWait(context.browser, 10).until(
        ec.presence_of_all_elements_located((By.CLASS_NAME, "comment-content-lg")),
    )
    assert len(comments) == count


@then("each comment should display")
def check_comment_info(context):
    comments = context.browser.find_elements(By.CLASS_NAME, "comment")
    for comment in comments:
        for row in context.table:
            assert comment.find_element(
                By.CLASS_NAME,
                row["Information"].lower().replace(" ", "-"),
            )
