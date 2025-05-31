from django.core.management import call_command
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_feature(context, feature):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_experimental_option("detach", value=True)

    context.browser = webdriver.Chrome(options=options)


def after_feature(context, feature):
    context.browser.quit()
    call_command("flush", "--noinput")
