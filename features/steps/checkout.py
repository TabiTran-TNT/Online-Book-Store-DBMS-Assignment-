import os

from behave import given, then, when
from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.tests.factories import BookFactory
from bookstore_binht.order.models import Order
from bookstore_binht.users.tests.factories import UserFactory


@given("I am a registered user")
def create_use_and_login(context):
    context.user = UserFactory()
    context.book = BookFactory()
    context.browser.get(context.get_url(reverse("home")))
    context.browser.find_element(By.ID, "log-in-link").click()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    context.browser.find_element(By.NAME, "login").send_keys(context.user.email)
    context.browser.find_element(By.NAME, "password").send_keys(
        os.getenv("USER_PASSWORD", "06112003"),
    )

    submit_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#login button[type="submit"]')),
    )

    submit_button.click()


@given("I have added items to my shopping cart")
def add_items(context):
    wait = WebDriverWait(context.browser, 10)
    add_to_cart_button = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".btn.custom-button.add-to-cart")),
    )

    try:
        add_to_cart_button.click()
    except StaleElementReferenceException:
        add_to_cart_button = wait.until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.custom-button.add-to-cart"),
            ),
        )
        add_to_cart_button.click()


@when("I navigate to the shopping cart page")
def visit_shopping_cart_page(context):
    context.execute_steps(
        """
        When I visit cart detail page
        """,
    )


@when("I choose to checkout")
def checkout(context):
    checkout_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "checkoutButton")),
    )
    checkout_button.click()


@then("I should be directed to the checkout page")
def check_url_checkout(context):
    WebDriverWait(context.browser, 10).until(
        ec.url_contains(reverse("order:checkout")),
    )


@given("I am an anonymous user")
def anonymous_condtition(context):
    context.book = BookFactory()
    context.browser.get(context.get_url(reverse("home")))


@then("the login modal will pop up")
def check_login_modal(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )


@then('I see the message "{checkout_msg}" on the modal')
def checkout_msg(context, checkout_msg):
    message = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "checkoutMessage1")),
    )
    assert message.text == checkout_msg


@then("I fill the following information")
def fill_shipping_form(context):
    for row in context.table:
        field = row["Field"]
        value = row["Value"]
        context.browser.find_element(By.NAME, field).send_keys(value)


@then("I click Proceed button")
def click_proceed_button(context):
    button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "proceedButton")),
    )
    button.click()


@then("I click Place Order button")
def click_place_order(context):
    checkbox = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[type="checkbox"][value="cash"]'),
        ),
    )
    checkbox.click()

    place_order_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "placeOrderButton")),
    )
    place_order_button.click()


@then("the order details should be stored into the database")
def check_order_db(context):
    assert Order.objects.get(user=context.user) is not None
