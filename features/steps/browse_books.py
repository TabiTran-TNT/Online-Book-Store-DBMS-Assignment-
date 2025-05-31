from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.models import Book, Category
from bookstore_binht.books.tests.factories import BookFactory, CategoryFactory


@when("I visit the home page")
def step_visit_home_page(context):
    context.browser.get(context.get_url("/"))


@given("the following categories exist for browsing")
def add_categories(context):
    for row in context.table:
        CategoryFactory(name=row["Category Name"])

    # Verify the number of categories created
    expected_count = len(context.table.rows)
    actual_count = Category.objects.count()
    assert (
        actual_count == expected_count
    ), f"Expected {expected_count} categories, but got {actual_count}"


@given("the following books exist")
def add_books(context):
    for row in context.table:
        book = BookFactory(title=row["Title"])
        category_names = [category.strip() for category in row["Categories"].split(",")]
        for category_name in category_names:
            category, _ = Category.objects.get_or_create(name=category_name)
            book.categories.add(category)

    # Verify the number of books created
    expected_count = len(context.table.rows)
    actual_count = Book.objects.count()
    assert (
        actual_count == expected_count
    ), f"Expected {expected_count} books, but got {actual_count}"


@then("I should see a list of all available categories")
def check_category_list(context):
    category_list = context.browser.find_elements(By.NAME, "category-list")
    assert category_list is not None, "Category list not found"


@when("I visit the book browsing page")
def visit_bookpage(context):
    context.browser.get(context.get_url("/"))


@when('I select the "{category_name}" category')
def select_category(context, category_name):
    wait = WebDriverWait(context.browser, 10)
    category_link = wait.until(
        ec.element_to_be_clickable((By.LINK_TEXT, category_name)),
    )
    category_link.click()


@then('I select the "{category_name}" category')
def select_book_category(context, category_name):
    wait = WebDriverWait(context.browser, 10)
    category_link = wait.until(
        ec.element_to_be_clickable((By.LINK_TEXT, category_name)),
    )
    category_link.click()


@then('I should see a list of books in the "{category_name}" category')
def check_categorized_book(context, category_name):
    book_items = context.browser.find_elements(By.NAME, "book-item")
    assert book_items is not None, "Book list not found"


@then('the list should include "{book_title}"')
def check_content_categorized_book(context, book_title):
    assert context.browser.find_element(
        By.XPATH,
        f"//*[contains(text(), '{book_title}')]",
    ), f"Book title '{book_title}' not found on the page"


@then('I should see a message saying "{message}"')
def check_no_book_msg(context, message):
    wait = WebDriverWait(context.browser, 10)
    message_element = wait.until(
        ec.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{message}')]"),
        ),
    )
    assert message_element, f"Message '{message}' not found on the page"
