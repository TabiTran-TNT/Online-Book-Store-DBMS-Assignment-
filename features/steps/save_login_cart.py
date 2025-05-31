from behave import given, then
from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.users.models import User
from bookstore_binht.users.tests.factories import UserFactory


@given('I am an authenticated user with email "{email}" and password "{password}"')
def login_user(context, email, password):
    try:
        context.user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = UserFactory(email=email, password=password)
        context.user = user

    if not hasattr(context, "book"):
        context.book = BookFactory()

    context.browser.get(context.get_url(reverse("home")))

    sign_in = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "log-in-link")),
    )
    sign_in.click()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    context.browser.find_element(By.ID, "id_login").send_keys(email)
    context.browser.find_element(By.ID, "id_password").send_keys(password)

    submit_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#login button[type="submit"]')),
    )
    submit_button.click()


@given("I am at detail page of a book")
def browse_detail_book(context):
    home_logo_link = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.NAME, "home-logo")),
    )
    try:
        home_logo_link.click()
    except StaleElementReferenceException:
        home_logo_link = WebDriverWait(context.browser, 10).until(
            ec.element_to_be_clickable((By.NAME, "home-logo")),
        )
        home_logo_link.click()
    book_link = context.browser.find_element(By.NAME, "book-title")
    book_link.click()


@then("I should see the item in cart detail page")
def step_impl(context):
    context.execute_steps(
        """
        When I visit cart detail page
        Then I should see the order of the book I added
        """,
    )


@then("I sign out and log in again")
def signout_and_login(context):
    user_info_icon = context.browser.find_element(By.NAME, "user-info")
    user_info_icon.click()

    logout_link = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "log-out-link")),
    )
    logout_link.click()

    signout_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "logoutButtonModal")),
    )

    signout_button.click()

    context.execute_steps(
        """
        Given I am an authenticated user with"""
        """ email "user@gmail.com" and password "password"
        """,
    )


@then("I visit cart detail page")
def browse_cart_detail(context):
    wait = WebDriverWait(context.browser, 10)
    icon_cart = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".bi-cart2")),
    )
    try:
        icon_cart.click()
    except StaleElementReferenceException:
        icon_cart = wait.until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".bi-cart2")),
        )
        icon_cart.click()


@then("I still can see the item in cart detail page")
def check_cart_logged_in(context):
    context.execute_steps(
        """
        Then I should see the order of the book I added
        """,
    )


@given("I am an anonymous user at detail page of a book")
def anonymous_browse_detail(context):
    if not hasattr(context, "book"):
        context.book = BookFactory()

    context.browser.get(context.get_url(reverse("home")))
    context.execute_steps(
        """
        Given I am at detail page of a book
        """,
    )


@then('I sign in with email "{email}" and password "{password}"')
def sign_in_step(context, email, password):
    context.execute_steps(
        """
        Given I am an authenticated user with"""
        """ email "user@gmail.com" and password "password"
        """,
    )


@then("I sign out and add a book to cart as an anonymous user")
def signout_and_add_book(context):
    user_info_icon = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.NAME, "user-info")),
    )
    user_info_icon.click()

    logout_link = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "log-out-link")),
    )
    logout_link.click()

    signout_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "logoutButtonModal")),
    )

    signout_button.click()

    WebDriverWait(context.browser, 10).until(
        ec.presence_of_element_located((By.ID, "log-in-link")),
    )

    context.execute_steps(
        """
        Given I am an anonymous user at detail page of a book
        When I click on the "Add to Cart" button
        """,
    )


@then("I sign in again")
def signin_step(context):
    context.execute_steps(
        """
        Given I am an authenticated user with"""
        """ email "user@gmail.com" and password "password"
        """,
    )


@then("I should see items with quantity of {expected_quantity:d}")
def check_item_quantity(context, expected_quantity):
    context.execute_steps(
        f"""
        Then the quantity should be {expected_quantity}
        """,
    )
