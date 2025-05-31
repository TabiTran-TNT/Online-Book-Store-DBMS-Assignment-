import time

from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.users.models import User
from bookstore_binht.users.tests.factories import UserFactory


@given("the user open the login modal")
def open_login_modal(context):
    if User.objects.count() == 0:
        UserFactory()
    context.browser.get(context.get_url("/"))
    context.browser.find_element(By.ID, "log-in-link").click()
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )


@when("the user enters incorrect username/password combination three times")
def type_wrong_credentials_3_times(context):
    wait = WebDriverWait(context.browser, 10)
    context.browser.find_element(By.NAME, "login").send_keys("binh.tran0611@gmail.com")
    context.browser.find_element(By.NAME, "password").send_keys("wrongpassword")
    submit_button = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#login button[type="submit"]')),
    )
    for _i in range(3):
        submit_button.click()
        time.sleep(1)

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "#login-error:not(.d-none)"),
        ),
    )

    error_elements = context.browser.find_elements(
        By.CSS_SELECTOR,
        "#login-error:not(.d-none)",
    )
    assert error_elements[0].text == "Invalid credentials or captcha"


@then("the user should be prompted to validate with a Captcha")
def check_captcha_appear(context):
    captcha_collect = context.browser.find_elements(By.ID, "captcha-container")
    assert captcha_collect is not None
