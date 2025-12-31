import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import get_driver,generate_unique_username

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture
def valid_signup_data():
    return {
        "email": generate_unique_username() + "@naver.com",
        "password": "@qa12345",
        "name": "김성호"
    }