from behave import given, then, when
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.tests.factories import BookFactory


@given("I am at the home page as anonymous user")
def browse_home_anonymous_user(context):
    context.book = BookFactory()
    context.browser.get(context.get_url(reverse("home")))


@when("there is only 15 minutes left in my session")
def simulate_session_expiry(context):
    context.browser.execute_script("""
        const newExpiryTime = 15 * 60 * 1000 + 5000;
        const sessionExpiry = SessionExpiry.instance;
        if (sessionExpiry) {
            sessionExpiry.sessionExpiryTime = newExpiryTime;
            sessionExpiry.showModalTime = newExpiryTime - sessionExpiry.warningTime;
            sessionExpiry.start();
        }
    """)


@then("I should see login modal pops up")
def check_login_modal(context):
    # Wait for the modal to appear
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )
    assert context.browser.find_element(By.ID, "login").is_displayed()


@then("I should see the UI change to indicate the session is about to expire")
def check_ui_change(context):
    # Check that the UI elements have changed
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "cartExpireTitle")),
    )
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "checkoutCloseButtonLogin")),
    )
