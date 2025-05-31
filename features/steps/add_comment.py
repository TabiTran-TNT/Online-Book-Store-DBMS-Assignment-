from behave import given, then, when
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.models import Book
from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.users.models import User
from bookstore_binht.users.tests.factories import UserFactory


@given("a user with email '{email}' and password '{password}' exists")
def ensure_user_exists(context, email, password):
    try:
        context.user = User.objects.get(email=email)
    except User.DoesNotExist:
        context.user = UserFactory(email=email, password=password)
    context.password = password


@given("there is a book in the database with the following details for comment test")
def step_create_book(context):
    for row in context.table:
        BookFactory(
            title=row["Title"],
            author_name=row["Author"],
            publisher_name=row["Publisher"],
            published_date=row["Published Date"],
            unit_price=float(row["Price"]),
        ).save()
        context.book = Book.objects.get(title=row["Title"])


@given('I am on the book comment page for "{book_title}" for comment test')
def navigate_to_book_details(context, book_title):
    book = Book.objects.get(title=book_title)
    context.browser.get(
        context.get_url(reverse("books:book_comments", kwargs={"pk": book.id})),
    )


@given("I am on the login page")
def navigate_to_login_page(context):
    context.browser.get(context.get_url(reverse("account_login")))


@when('I fill in "{field_id}" with "{value}"')
def fill_in_field(context, field_id, value):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )
    input_field = context.browser.find_element(By.ID, field_id)
    input_field.send_keys(value)


@when('I click the "{button_text}" button')
def click_button(context, button_text):
    WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')),
    )
    button = context.browser.find_element(
        By.CSS_SELECTOR,
        '#login button[type="submit"]',
    )
    button.click()


@given('I am logged in as "{email}" with password "{password}"')
def login_to_account(context, email, password):
    context.execute_steps("Given I am on the login page")
    context.execute_steps(
        f"""
        When I fill in "id_login" with "{email}"
        And I fill in "id_password" with "{password}"
        And I click the "SIGN IN" button
        """,
    )


@when('I click on the "Write a review" button')
@given('I click on the "Write a review" button')
def step_impl(context):
    write_review_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "reviewButton1")),
    )
    write_review_button.click()


@when('I add a rating of "{rating}" and a comment "{comment}"')
def add_rating_and_comment(context, rating, comment):
    WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "i.star.far.fa-star.fs-2")),
    )
    rating_stars = context.browser.find_elements(
        By.CSS_SELECTOR,
        "i.star.far.fa-star.fs-2",
    )
    rating_stars[int(rating) - 1].click()

    comment_textarea = context.browser.find_element(By.ID, "id_content")
    comment_textarea.send_keys(comment)

    submit_button = context.browser.find_element(
        By.XPATH,
        '//button[text()="ADD REVIEW"]',
    )
    submit_button.click()


@then("I should see my comment '{comment}' with rating '{rating}'")
def verify_comment_added(context, comment, rating):
    comment_found = WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located(
            (By.CSS_SELECTOR, "p.comment-content-lg.col-lg-12"),
        ),
    )

    assert comment in comment_found.text, comment_found.text


@then("I should see pop up modal informing I can only comment once")
def verify_cannot_add_multiple_comments(context):
    alert_comment_modal = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.ID, "commentModal"),
        ),
    )
    assert alert_comment_modal.is_displayed()


@when("I try to add a rating and a comment")
def try_to_add_rating_and_comment(context):
    rating_stars = WebDriverWait(context.browser, 2).until(  # Short wait
        ec.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "i.star.far.fa-star.fs-2"),
        ),
    )
    rating_stars[3].click()  # Try to click a star

    comment_textarea = context.browser.find_element(By.ID, "id_content")
    comment_textarea.send_keys("Another comment attempt")

    submit_button = context.browser.find_element(
        By.XPATH,
        '//button[text()="Post Comment"]',
    )
    submit_button.click()


@when("I try to add a rating and a comment again")
def try_add_rating_and_comment_again(context):
    context.execute_steps(
        """
        When I click on the "Write a review" button
        """,
    )
    context.execute_steps(
        """
        When I add a rating of "5" and a comment "This is another comment."
        """,
    )


@then(
    'I should see an error message "{error_message}"',
)
def verify_error_message(context, error_message):
    error_element = WebDriverWait(context.browser, 5).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, ".alert.alert-dismissible.alert-error"),
        ),
    )
    assert error_message in error_element.text


@given("I am an unauthenticated user")
def context_build(context):
    # This step is just a placeholder to build the context
    pass


@when('I click on the "Write a review" button for anonymous users')
def click_review_anonymous(context):
    write_review_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "loginReview1")),
    )
    write_review_button.click()


@then("I should see the login modal appear with notification to log in to comment")
def check_login_modal_pop_up(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    login_title = context.browser.find_element(By.ID, "loginTitle")
    close_button = context.browser.find_element(By.ID, "closeButtonLogin")
    cart_expire_title = context.browser.find_element(By.ID, "reviewLoginTitle")
    checkout_close_button = context.browser.find_element(
        By.ID,
        "checkoutCloseButtonLogin",
    )
    login_modal_header = context.browser.find_element(By.ID, "loginModalHeader")

    assert "d-none" in login_title.get_attribute("class")
    assert "d-none" in close_button.get_attribute("class")
    assert "d-none" not in cart_expire_title.get_attribute("class")
    assert "d-none" not in checkout_close_button.get_attribute("class")
    assert "review-login-header" in login_modal_header.get_attribute("class")
