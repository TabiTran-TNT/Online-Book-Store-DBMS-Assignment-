# conftest.py
import pytest


@pytest.fixture()
def user_password():
    return "password123@"
