from behave import given, then, when
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bookstore_binht.books.tests.factories import BookFactory


@given("I am an user at detail page of a book")
def browse_detail_page(context):
    book = BookFactory()
    context.book = book

    context.browser.get(context.get_url(reverse("books:book_detail", args=[book.id])))


@when('I click on the "Add to Cart" button')
def click_add_to_cart(context):
    wait = WebDriverWait(context.browser, 10)
    add_to_cart_button = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".btn.custom-button.add-to-cart")),
    )

    add_to_cart_button.click()


@then("I should see the cart display number 1")
def check_number_display(context):
    cart_badge = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".bi-cart2 span.badge")),
    )
    assert cart_badge.text == "1"


@when("I visit cart detail page")
def browse_cart_detail(context):
    wait = WebDriverWait(context.browser, 10)
    icon_cart = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".bi-cart2")),
    )
    icon_cart.click()


@then("I should see the order of the book I added")
def check_added_book_presented_in_cart_page(context):
    book = context.book
    items = context.browser.find_elements(By.NAME, "book-item")
    assert len(items) == 1
    assert items[0].find_element(By.NAME, "book-title").text == book.title
    assert items[0].find_element(By.NAME, "book-quantity").text == "1"
    assert (
        items[0].find_element(By.NAME, "unit-price").text
        in f"${book.get_formatted_price()}"
    )


@then("I click the remove button")
@when("I click the remove button")
def click_remove_button(context):
    remove_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "button.btn.cart-button.delete-cart-item[type='submit'][data-book-id]",
            ),
        ),
    )
    remove_button.click()


@then("order should be deleted")
def check_order_is_deleted(context):
    items = context.browser.find_elements(By.NAME, "book-item")
    assert len(items) == 0


@then("the number should be disappeared on the cart icon")
def check_disappeared_number(context):
    WebDriverWait(context.browser, 10).until(
        ec.invisibility_of_element_located((By.CSS_SELECTOR, ".bi-cart2 span.badge")),
    )

    assert not context.browser.find_elements(By.CSS_SELECTOR, ".bi-cart2 span.badge")


@when("I click the increase button")
def click_increase_button(context):
    increase_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btn.add-to-cart[type='button']"),
        ),
    )
    increase_button.click()


@then("the quantity should be {expected_quantity:d}")
def check_increased_quantity(context, expected_quantity):
    quantity_element = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div[name='book-quantity']"),
        ),
    )

    quantity_text = quantity_element.text.strip()

    assert quantity_text == str(
        expected_quantity,
    ), f"Expected quantity to be '{expected_quantity}', but got '{quantity_text}'"


@then("the total price should be updated")
def check_total_price(context):
    unit_price = context.book.unit_price

    quantity = 2

    expected_total_price = round(unit_price * quantity)

    total_price_element = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.price.total-cart-price"),
        ),
    )

    total_price_text = total_price_element.text.strip()

    total_price_value = int(total_price_text.replace("đ", "").replace(",", "").strip())

    assert total_price_value == expected_total_price, (
        f"Expected total price to be '{expected_total_price}', "
        f"but got '{total_price_value}'"
    )


@then("the number should be updated on the cart icon")
def check_updated_number(context):
    cart_badge = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".bi-cart2 span.badge")),
    )
    assert cart_badge.text == "2"


@when("I click the decrease button")
def click_decrease_button(context):
    decrease_button = WebDriverWait(context.browser, 10).until(
        ec.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btn.decrease-from-cart[type='button']"),
        ),
    )
    decrease_button.click()


@then('I should see the message "{expected_message}"')
def check_empty_cart_msg(context, expected_message):
    empty_cart_msg_element = WebDriverWait(context.browser, 10).until(
        ec.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "p.my-5",
            ),  # Selecting the paragraph element with class my-5
        ),
    )

    empty_cart_msg_text = empty_cart_msg_element.text.strip()

    assert empty_cart_msg_text == expected_message
