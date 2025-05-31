import datetime
import os

from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.users.models import User


def fill_in_form(context, return_email):
    email = None
    wait = WebDriverWait(context.browser, 10)
    for row in context.table:
        field = row["Field"].lower()
        value = row["Value"]
        if field == "full name":
            context.browser.find_element(By.NAME, "name").send_keys(value)
            context.name = value
        else:
            context.browser.find_element(By.NAME, field).send_keys(value)
        if field == "email" and return_email:
            email = value

    submit_button = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#signUp button[type="submit"]')),
    )
    submit_button.click()
    if return_email:
        return email
    return None


@given("I am an anonymous user and I open sign up modal")
def visit_sign_up_page(context):
    context.browser.get(context.get_url("/"))
    context.current_url = context.browser.current_url
    context.browser.find_element(By.ID, "log-in-link").click()
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "sign-up-access")),
    )
    context.browser.find_element(By.ID, "sign-up-access").click()


@then(
    "I should see a form with following information: "
    "Email, Password, Phone, Full name, Birthday",
)
def check_sign_up_fields(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "signUp")),
    )

    email = context.browser.find_element(By.NAME, "email")
    phone = context.browser.find_element(By.NAME, "phone")
    full_name = context.browser.find_element(By.NAME, "name")
    birth_day = context.browser.find_element(By.NAME, "birth_day")
    birth_month = context.browser.find_element(By.NAME, "birth_month")
    birth_year = context.browser.find_element(By.NAME, "birth_year")
    password1 = context.browser.find_element(By.NAME, "password1")
    password2 = context.browser.find_element(By.NAME, "password2")
    assert email.is_displayed()
    assert phone.is_displayed()
    assert full_name.is_displayed()
    assert birth_day.is_displayed()
    assert birth_month.is_displayed()
    assert birth_year.is_displayed()
    assert password1.is_displayed()
    assert password2.is_displayed()


@when("I fill in necessary and valid information")
def fill_sign_up_form(context):
    context.email = fill_in_form(context, return_email=True)


@then("the pop up modal inform verification email has been sent")
def check_pop_up_modal_verification(context):
    activate_modal = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "accountActivateModal")),
    )
    assert activate_modal.is_displayed()

    modal_body = context.browser.find_element(
        By.CSS_SELECTOR,
        "#accountActivateModal .modal-body",
    )
    expected_content = (
        f"Hi {context.name}, Thanks for joining us. "
        "Please go to your email to activate your account."
    )
    assert expected_content in modal_body.text


@then("I will be directed to current page")
def check_direct_after_registration(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")),
    )
    assert context.browser.current_url == context.current_url


@then("my information should be stored in the system")
def check_user_info_stored_or_not(context):
    # This is to make sure the model is updated at backend for BDD test
    user = User.objects.get(email=context.email)
    assert user is not None


@when("I fill in some invalid fields")
def fill_invalid_sign_up_form(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "signUp")),
    )
    fill_in_form(context, return_email=False)


@then("I should see the error messages and the format it should be")
def check_signup_form_err_msg(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.align-middle.alert:not(.d-none)"),
        ),
    )

    error_elements = context.browser.find_elements(
        By.CSS_SELECTOR,
        "div.align-middle.alert:not(.d-none)",
    )

    assert error_elements[0].text == "Enter a valid email address."
    assert error_elements[1].text == "You must type the same password each time."
    assert error_elements[2].text == "Invalid phone number."
    assert error_elements[3].text == "Invalid date."


@when("I fill in an already used email")
def fill_used_email(context):
    password = os.getenv("TEST_EXIST_USER_PASSWORD", "hello@123")
    User.objects.create_user(
        email="binh.tran0611csbk@hcmut.edu.vn",
        password=password,
        phone="0859007204",
        birthday=datetime.date(2003, 11, 6),
        name="Binh Tran",
    ).save()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "signUp")),
    )

    fill_in_form(context, return_email=False)


@then(
    "I should see the error messages"
    ' "A user is already registered with this email address."',
)
def check_used_email_err_msg(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.align-middle.alert:not(.d-none)"),
        ),
    )

    error_elements = context.browser.find_elements(
        By.CSS_SELECTOR,
        "div.align-middle.alert:not(.d-none)",
    )
    assert (
        error_elements[0].text
        == "A user is already registered with this email address."
    )
