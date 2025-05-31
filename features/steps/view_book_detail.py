from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


@given("the following categories exist")
def add_categories(context):
    context.execute_steps(
        """
            Given the following categories exist for browsing
                | Category Name |
                | Fiction       |
            """,
    )


@given("I am on the home page")
def visit_homepage(context):
    context.browser.get(context.get_url("/"))


@when("I click on the book title to visit its detail")
def click_book_title(context):
    wait = WebDriverWait(context.browser, 10)
    book_title_link = wait.until(
        ec.element_to_be_clickable((By.NAME, "book-title")),
    )

    book_title_link.click()


@then("I should see all information about the book")
def verify_book_detail(context):
    book_title = context.browser.find_element(By.NAME, "book-title")
    book_photo = context.browser.find_element(By.NAME, "book-photo")
    button_price = context.browser.find_element(By.NAME, "button-price")
    book_rating = context.browser.find_element(By.NAME, "book-rating")
    book_description = context.browser.find_element(By.ID, "book-description")
    book_detail = context.browser.find_element(By.NAME, "book-detail")
    book_review = context.browser.find_element(By.NAME, "book-review")

    assert book_title is not None
    assert book_photo is not None
    assert button_price is not None
    assert book_rating is not None
    assert book_description is not None
    assert book_detail is not None
    assert book_review is not None
