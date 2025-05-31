from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.models import Book
from bookstore_binht.order.models import Order, OrderItem
from bookstore_binht.order.tests.factories import OrderItemFactory, OrderModelFactory
from bookstore_binht.users.models import User

NUM_ORDERS = 2


@given("I am a registered user with one order in the past")
def setup_past_order(context):
    context.order = OrderModelFactory()
    context.order_item = OrderItemFactory(order=context.order)
    context.book = context.order_item.book

    assert User.objects.count() == 1
    assert User.objects.first().email == "binh.tran0611csbk@hcmut.edu.vn"
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1
    assert Book.objects.count() == 1

    context.browser.get(context.get_url("/"))
    login_toggle = context.browser.find_element(By.ID, "log-in-link")
    login_toggle.click()

    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "login")),
    )

    email_input = context.browser.find_element(By.ID, "id_login")
    email_input.send_keys("binh.tran0611csbk@hcmut.edu.vn")
    password_input = context.browser.find_element(By.ID, "id_password")
    password_input.send_keys("06112003")

    submit_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#login button[type="submit"]')),
    )
    submit_button.click()

    # Wait for visibility of <i class="bi bi-person icon-large"></i>
    WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.CLASS_NAME, "bi-person")),
    )


@when("I visit the order history page")
def visit_order_history_page(context):
    user_icon = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CLASS_NAME, "bi-person")),
    )
    user_icon.click()
    past_order_link = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.NAME, "order-history-dropdown")),
    )
    past_order_link.click()


@then("I should see the order")
def check_past_order(context):
    order = context.browser.find_element(By.NAME, f"order-date-{context.order.id}")
    assert order is not None


@then("I click the chevron icon")
def click_chevron_icon(context):
    chevron_icon = context.browser.find_element(By.ID, f"order-icon-{context.order.id}")
    chevron_icon.click()


@then("I should see the order details")
def check_order_details(context):
    order_item = context.browser.find_element(
        By.NAME,
        f"order-item-{context.order_item.id}",
    )
    assert order_item is not None


@then("I navigate to homepage and make a purchase")
def navigate_homepage(context):
    home_logo = context.browser.find_element(By.NAME, "home-logo")
    home_logo.click()

    button_price = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CLASS_NAME, "add-to-cart")),
    )
    button_price.click()

    cart_icon = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.NAME, "cart-icon")),
    )
    cart_icon.click()

    checkout_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "checkoutButton")),
    )
    checkout_button.click()

    shipping_address = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_shipping_address")),
    )
    shipping_address.send_keys("123 ABC Street")

    city = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_city")),
    )
    city.send_keys("Ho Chi Minh")

    zip_code = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_zip_code")),
    )
    zip_code.send_keys("700000")

    country = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.ID, "id_country")),
    )
    country.send_keys("Vietnam")

    proceed_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CLASS_NAME, "proceed-button")),
    )
    proceed_button.click()

    cash_payment = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="cash"]')),
    )
    cash_payment.click()

    place_order_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.ID, "placeOrderButton")),
    )

    place_order_button.click()

    WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable((By.NAME, "home-button")),
    ).click()

    WebDriverWait(context.browser, 10).until(
        ec.url_to_be(context.get_url("/")),
    )


@then("I navigate to order history page")
def visit_order_history_page_again(context):
    context.execute_steps("""
        When I visit the order history page
    """)


@then("I should see the new order")
def check_new_order(context):
    order_items = context.browser.find_elements(
        By.XPATH,
        "//*[contains(@name, 'order-date-')]",
    )
    assert len(order_items) == NUM_ORDERS
