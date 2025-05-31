from decimal import Decimal
from urllib.parse import parse_qs, urlparse

from behave import given, then, when
from django.utils import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from bookstore_binht.books.tests.factories import BookFactory


@given("there are {num_books:d} books in the database")
def step_create_books(context, num_books):
    for book_id in range(1, num_books + 1):
        BookFactory(
            title=f"Book {book_id}",
            description=f"Description for Book {book_id}",
            author_name=f"Author {book_id}",
            publisher_name=f"Publisher {book_id}",
            published_date=timezone.now(),
            unit_price=Decimal(f"{book_id + 10}.99"),
            total_rating_value=book_id * 5,
            total_rating_count=book_id,
        )


@when("I visit the home page for pagination")
def step_visit_home_page(context):
    context.browser.get(context.get_url("/"))


@when('I visit the home page with a query parameter "{param}"')
def step_visit_home_page_with_param(context, param):
    url = context.get_url(f"/?{param}")
    context.browser.get(url)


@when('I click on the "{link_text}" page link')
def step_click_page_link(context, link_text):
    link = context.browser.find_element(By.LINK_TEXT, link_text)
    link.click()


@when("I click on the last page number")
def step_click_last_page(context):
    pagination = context.browser.find_element(By.CLASS_NAME, "pagination")
    last_page_link = pagination.find_elements(By.TAG_NAME, "a")[-1]
    last_page_link.click()


@then("I should see pagination controls")
def step_check_pagination_controls(context):
    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")),
    )

    pagination = context.browser.find_element(By.CSS_SELECTOR, "ul.pagination")

    first_page = pagination.find_element(
        By.XPATH,
        ".//li/a[contains(@class, 'page-link') and .//span[contains(text(), 'First')]]",
    )
    prev_page = pagination.find_element(
        By.XPATH,
        ".//li/a[contains(@class, 'page-link') and .//span[contains(text(), 'Prev')]]",
    )
    next_page = pagination.find_element(
        By.XPATH,
        ".//li/a[contains(@class, 'page-link') and .//span[contains(text(), 'Next')]]",
    )
    last_page = pagination.find_element(
        By.XPATH,
        ".//li/a[contains(@class, 'page-link') and .//span[contains(text(), 'Last')]]",
    )

    numbered_pages = pagination.find_elements(
        By.XPATH,
        ".//li[contains(@class, 'page-item')]/a[contains(@class, 'page-link')"
        " and string-length(text()) = 1]",
    )

    assert pagination.is_displayed(), "Pagination controls are not displayed"
    assert first_page.is_displayed(), "First page link is not displayed"
    assert prev_page.is_displayed(), "Previous page link is not displayed"
    assert next_page.is_displayed(), "Next page link is not displayed"
    assert last_page.is_displayed(), "Last page link is not displayed"
    assert len(numbered_pages) > 0, "No numbered page links found"


@then("the page should indicate it is page {page_num:d} of {total_pages:d}")
def step_check_page_indication(context, page_num, total_pages):
    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")),
    )

    pagination = context.browser.find_element(By.CSS_SELECTOR, "ul.pagination")

    active_page = pagination.find_element(By.CSS_SELECTOR, "li.page-item.active")
    current_page = int(active_page.text.strip())

    last_page_link = pagination.find_elements(
        By.CSS_SELECTOR,
        "li.page-item:not(.disabled) .page-link",
    )[-1]
    last_page_url = last_page_link.get_attribute("href")
    parsed_url = urlparse(last_page_url)
    query_params = parse_qs(parsed_url.query)
    last_page_number = int(query_params.get("page", [1])[0])

    assert (
        current_page == page_num
    ), f"Expected to be on page {page_num}, but found page {current_page}"
    assert (
        last_page_number == total_pages
    ), f"Expected {total_pages} total pages, but found {last_page_number}"


@then("I should see an error message")
def step_check_error_message(context):
    error_title = WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.TAG_NAME, "h1")),
    )

    assert error_title.is_displayed()
    assert error_title.text == "Page not found"


@then('I select "{page_size}" items per page from the dropdown')
@when('I select "{page_size}" items per page from the dropdown')
def step_select_items_per_page(context, page_size):
    dropdown = WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.NAME, "per_page")),
    )
    select = Select(dropdown)
    select.select_by_value(page_size)


@then("I should see {num:d} books listed")
def step_check_books_listed(context, num):
    books = WebDriverWait(context.browser, 10).until(
        ec.presence_of_all_elements_located((By.NAME, "book-item")),
    )
    assert len(books) == num


@then("the dropdown should show options for 10, 20, 30, and 40 items per page")
def step_check_per_page_options(context):
    dropdown = context.browser.find_element(By.NAME, "per_page")
    select = Select(dropdown)
    options = [option.get_attribute("value") for option in select.options]
    expected_options = ["10", "20", "30", "40"]
    assert set(options) == set(expected_options)
