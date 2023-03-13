import pytest
import requests
from playwright.sync_api import Page, expect


# Фикстура для выполнения запросов к API
@pytest.fixture(scope="module")
def api_client():
    session = requests.Session()
    return session


# Фикстура с базовым URL
@pytest.fixture
def api_url():
    API_URL = "https://reqres.in/api/"
    return API_URL


# Фикстура для последнего теста API
@pytest.fixture
def tear_down():
    yield
    print(" Тестирование API завершено \n ")


# Фикстура для веб-тестов
@pytest.fixture
def set_up_tear_down(page: Page) -> None:
    page.goto("https://reqres.in/")
    yield page
    print(" ТЕСТ прошел")


@pytest.fixture
def api_web_assert(api_client, api_url):
    response = api_client.post(f'{api_url}"users"', data={"name": "morpheus", "job": "leader"}, verify=False)
    return response
