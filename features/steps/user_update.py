from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


@given("the user is logged in")
def login(context):
    context.execute_steps("Given I am on the login page")
    context.execute_steps(
        f"""
        When I fill in "id_login" with "{context.user.email}"
        And I fill in "id_password" with "{context.password}"
        And I click the "SIGN IN" button
        """,
    )


@given('the user click "My Profile" page')
def browse_profile(context):
    context.browser.find_element(By.NAME, "user-info").click()
    profile_link = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.LINK_TEXT, "My Profile")),
    )
    profile_link.click()


@when("the user chooses to update their password")
def choose_update_pass(context):
    update_pass_link = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                'i.bi.bi-pencil.edit-field[data-field-id="id_current_password"]',
            ),
        ),
    )
    update_pass_link.click()


@when("enters the current password along with a new password")
def enter_password(context):
    current_pass = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_current_password")),
    )
    current_pass.send_keys("testpassword")

    new_pass = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_password")),
    )
    new_pass.send_keys("newpassword")

    confirm_pass = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_confirm_password")),
    )
    confirm_pass.send_keys("newpassword")


@when("click the Save button")
def save_button_click(context):
    context.browser.find_element(
        By.CSS_SELECTOR,
        'button[type="submit"].btn.save-button.rounded-0',
    ).click()


@then("user will be logged out")
def check_logged_out(context):
    WebDriverWait(context.browser, 10).until(
        ec.url_contains("/?next=/"),
    )


@then("user can log in again with new password")
def check_log_in_new_password(context):
    context.browser.get(context.get_url("/"))
    context.browser.find_element(By.LINK_TEXT, "SIGN IN").click()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    context.browser.find_element(By.NAME, "login").send_keys(context.user.email)
    context.browser.find_element(By.NAME, "password").send_keys("newpassword")
    context.browser.find_element(
        By.CSS_SELECTOR,
        '#login button[type="submit"]',
    ).click()


@when("the user chooses to update their email address with 'modifyuser@example.com'")
def choose_update_email(context):
    update_pass_link = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, 'i.bi.bi-pencil.edit-field[data-field-id="id_email"]'),
        ),
    )
    update_pass_link.click()

    email = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_email")),
    )
    email.clear()
    email.send_keys("modifyuser@example.com")


@then("the user's email address will be updated to 'modifyuser@example.com'")
def check_update_email(context):
    input_email = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_email")),
    )
    assert input_email.get_attribute("value") == "modifyuser@example.com"


@when("enters an incorrect current password")
def enter_wrong_passs(context):
    current_pass = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_current_password")),
    )
    current_pass.send_keys("wrongpassword")

    new_pass = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_password")),
    )
    new_pass.send_keys("newpassword")

    confirm_pass = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_confirm_password")),
    )
    confirm_pass.send_keys("newpassword")


@then('the error message "Current password is incorrect"')
def check_error_msg(context):
    error_msg = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.align-middle.alert.custom-error"),
        ),
    )
    assert error_msg.text == "Current password is incorrect."
