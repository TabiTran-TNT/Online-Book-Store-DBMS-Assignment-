import os

from allauth.account.models import EmailAddress
from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.users.models import User
from bookstore_binht.users.tests.factories import UserFactory


@given("the user is on homepage")
def setup_browse_home(context):
    password = os.environ.get("TEST_LOGIN_PASSWORD", default="06112003")

    if User.objects.count() == 0:
        context.user = UserFactory(password=password, email="binh.tran@eastagile.com")

    assert User.objects.count() == 1
    assert EmailAddress.objects.count() == 1
    assert EmailAddress.objects.first().verified
    context.browser.get(context.get_url("/"))


@given('the user open the login modal and click "Forgot your password"')
def open_pass_reset_modal(context):
    context.browser.find_element(By.ID, "log-in-link").click()

    forgot_password_link = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "password-reset-access")),
    )

    forgot_password_link.click()


@then("the password reset modal should be pop up")
def check_pass_reset_pop_up(context):
    modal_visible = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "resetPass")),
    )

    assert modal_visible.is_displayed()


@then("the user fill the valid email address and click submit button")
def fill_valid_email(context):
    email_input = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_email_reset")),
    )

    email_input.send_keys(context.user.email)

    submit_button = context.browser.find_element(By.ID, "passResetSubmit")
    submit_button.click()


@then("the success modal should be popped up")
def check_success_modal(context):
    modal_visible = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "resetPassDoneModal")),
    )

    assert modal_visible.is_displayed()


@then("the user fill the invalid email address and click submit button")
def fill_invalid_email(context):
    email_input = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_email_reset")),
    )
    email_input.send_keys("invalid_email@gmail.com")

    submit_button = context.browser.find_element(By.ID, "passResetSubmit")
    submit_button.click()


@then('the user should the error message "Invalid email"')
def check_reset_error(context):
    error_message = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "reset-error")),
    )

    assert error_message.is_displayed()
    assert error_message.text == "Invalid email"
