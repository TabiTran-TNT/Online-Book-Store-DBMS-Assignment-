import os

from allauth.account.models import EmailAddress
from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.users.models import User
from bookstore_binht.users.tests.factories import UserFactory


def fill_in_form(context):
    wait = WebDriverWait(context.browser, 10)
    for row in context.table:
        field = row["Field"].lower()
        value = row["Value"]
        if field == "username":
            context.email = value
            context.browser.find_element(By.NAME, "login").send_keys(value)
        else:
            context.browser.find_element(By.NAME, field).send_keys(value)

    submit_button = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#login button[type="submit"]')),
    )
    submit_button.click()


@given("I am an anonymous user on homepage and I visit sign in page")
def visit_sign_in_page(context):
    password = os.environ.get("TEST_LOGIN_PASSWORD", default="06112003")

    if User.objects.count() == 0:
        context.user = UserFactory(password=password)

    context.browser.get(context.get_url("/"))
    context.current_url = context.browser.current_url
    context.browser.find_element(By.ID, "log-in-link").click()


@then("I should see a form with following information: User name, Password")
def check_info_sign_in_page(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )
    email = context.browser.find_element(By.NAME, "login")
    password = context.browser.find_element(By.NAME, "password")
    assert email.is_displayed()
    assert password.is_displayed()


@when("I fill in correct username/password combination")
def fill_login_form(context):
    fill_in_form(context)


@when("I fill in incorrect username/password combination")
def fill_invalid_login_form(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    fill_in_form(context)


@when("I fill in unverified username/password combination")
def fill_unverified_login_form(context):
    email_address = EmailAddress.objects.get(user=context.user)
    email_address.verified = False
    email_address.save()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    fill_in_form(context)


@then('the user should be see the message "Invalid username and/or password"')
def check_err_msg_login(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "#login-error:not(.d-none)"),
        ),
    )

    error_elements = context.browser.find_elements(
        By.CSS_SELECTOR,
        "#login-error:not(.d-none)",
    )
    assert error_elements[0].text == "Invalid username and/or password"


@then("the pop up modal should appear informing the user to verify their email")
def check_pop_up_modal_not_verified(context):
    activate_modal = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "accountActivateModal")),
    )
    assert activate_modal.is_displayed()

    modal_body = context.browser.find_element(
        By.CSS_SELECTOR,
        "#accountActivateModal .modal-body",
    )
    expected_content = (
        "You haven't activated your account yet. "
        "Please go to your email to activate."
    )
    assert expected_content in modal_body.text, modal_body.text
