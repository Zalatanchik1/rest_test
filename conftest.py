import datetime

from faker import Faker
from requests import session

from constanta import HEADERS, BASE_URL
import pytest
import requests


faker = Faker()
@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации"
    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=10, max=1000),
        "depositpaid": bool(faker.pybool()),
        "bookingdates": {
            "checkin": faker.date_time().strftime("%Y-%m-%d"),
            "checkout": (faker.date_time() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        },
        "additionalneeds": faker.word()
    }

@pytest.fixture()
def booking_data_field_is_empty():
    return {
        "firstname": None,
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=10, max=1000),
        "depositpaid": bool(faker.pybool()),
        "bookingdates": {
            "checkin": faker.date_time().strftime("%Y-%m-%d"),
            "checkout": (faker.date_time() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        },
        "additionalneeds": faker.word()
    }