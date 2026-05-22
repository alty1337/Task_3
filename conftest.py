import pytest

from browser_factory import BrowserFactory
from helpers import create_user, delete_user, get_user_data


@pytest.fixture(params=["chrome", "firefox"], ids=["chrome", "firefox"])
def driver(request):
    browser = BrowserFactory.create_browser(request.param)
    browser.maximize_window()

    yield browser

    browser.quit()


@pytest.fixture
def user():
    payload = get_user_data()
    response = create_user(payload)
    token = response.json()["accessToken"]

    yield {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": token,
    }

    delete_user(token)
