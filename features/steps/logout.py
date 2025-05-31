import os

from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.users.models import User
from bookstore_binht.users.tests.factories import UserFactory


@given("I am an authenticated user")
def context_logout_setup(context):
    password = os.environ.get("TEST_LOGIN_PASSWORD", default="06112003")

    if User.objects.count() == 0:
        UserFactory(password=password).save()

    assert User.objects.count() == 1

    context.browser.get(context.get_url("/"))
    context.current_url = context.browser.current_url
    context.browser.find_element(By.ID, "log-in-link").click()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    context.browser.find_element(By.NAME, "login").send_keys(
        "binh.tran0611csbk@hcmut.edu.vn",
    )
    context.browser.find_element(By.NAME, "password").send_keys("06112003")

    submit_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#login button[type="submit"]')),
    )
    submit_button.click()


@when('I click on the "Sign out" button')
def signout_click(context):
    signout_button = WebDriverWait(context.browser, 50).until(
        ec.element_to_be_clickable((By.ID, "logout-sidebar")),
    )
    signout_button.click()


@then("I should see log out modal pop up")
def check_logout_modal_pop_up(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "logout")),
    )


@then('I click "Sign out" on the modal')
def signout_modal_click(context):
    WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "logoutButtonModal")),
    ).click()


@then("I should be logged out")
def check_status(context):
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "log-in-link")),
    )
