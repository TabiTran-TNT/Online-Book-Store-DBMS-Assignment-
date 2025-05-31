from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from bookstore_binht.books.models import Category
from bookstore_binht.books.tests.factories import BookFactory


@given("I am on the homepage")
def direct_homepage(context):
    context.browser.get(context.get_url("/"))


@given("the following books exist for searching")
def setup_book_category(context):
    for row in context.table:
        category, _ = Category.objects.get_or_create(name=row["category"])
        book = BookFactory(
            title=row["title"],
            author_name=row["author"],
        )
        book.categories.add(category)


@when('I enter "{search_term}" in the search bar')
def enter_search_context(context, search_term):
    search_input = context.browser.find_element(By.NAME, "search")
    search_input.clear()
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.RETURN)


@then('I should see a list of books whose title contains "{title_part}"')
def check_search_title(context, title_part):
    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "book-item")),
    )
    book_items = context.browser.find_elements(By.NAME, "book-item")
    assert len(book_items) > 0
    for item in book_items:
        title = item.find_element(By.NAME, "book-title").text
        assert title_part.lower() in title.lower()


@then(
    'I should see a list of books written by the author whose name is "{author_name}"',
)
def check_search_author(context, author_name):
    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "book-item")),
    )
    book_items = context.browser.find_elements(By.NAME, "book-item")
    assert len(book_items) > 0
    for item in book_items:
        author = item.find_element(By.NAME, "author-name").text
        assert author_name.lower() == author.lower()


@then('I should see a list of books whose title is "{title}" and author is "{author}"')
def check_search_title_and_author(context, title, author):
    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "book-item")),
    )
    book_items = context.browser.find_elements(By.NAME, "book-item")
    assert len(book_items) > 0
    for item in book_items:
        book_title = item.find_element(By.NAME, "book-title").text
        book_author = item.find_element(By.NAME, "author-name").text
        assert title.lower() == book_title.lower()
        assert author.lower() == book_author.lower()


@when('I select a category "{category_name}"')
def select_category(context, category_name):
    select_element = WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "category")),
    )

    select = Select(select_element)
    options = select.options

    for option in options:
        if category_name.lower() in option.text.lower():
            select.select_by_visible_text(option.text)


@then(
    'I should see a list of books in the "{category_name}" category'
    ' whose author is "{author_name}"',
)
def check_category_search(context, category_name, author_name):
    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "book-item")),
    )
    book_items = context.browser.find_elements(By.NAME, "book-item")
    assert len(book_items) == 1
    for item in book_items:
        author = item.find_element(By.NAME, "author-name").text
        assert author_name.lower() == author.lower()

    category_select = Select(context.browser.find_element(By.NAME, "category"))
    selected_category = category_select.first_selected_option.text
    assert category_name == selected_category
