import allure

from page_objects.login_page import LoginPage
from page_objects.main_page import MainPage
from page_objects.profile_page import ProfilePage
from urls import LOGIN_URL, ORDER_HISTORY_URL, PROFILE_URL


@allure.suite("Личный кабинет")
class TestProfile:
    @allure.title("Переход по клику на Личный Кабинет")
    def test_click_account_opens_profile(self, driver, user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)

        main_page.open()
        main_page.click_account_link()
        login_page.login(user["email"], user["password"])
        main_page.click_account_link()
        profile_page.wait_for_open_profile()

        assert PROFILE_URL in profile_page.get_current_url()

    @allure.title("Переход в раздел История заказов")
    def test_click_order_history_opens_order_history(self, driver, user):
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)

        login_page.open()
        login_page.login(user["email"], user["password"])
        profile_page.click_account_link()
        profile_page.click_order_history()
        profile_page.wait_for_open_order_history()

        assert ORDER_HISTORY_URL in profile_page.get_current_url()

    @allure.title("Выход из аккаунта")
    def test_logout_from_account(self, driver, user):
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)

        login_page.open()
        login_page.login(user["email"], user["password"])
        profile_page.click_account_link()
        profile_page.logout()
        profile_page.wait_for_url_contains(LOGIN_URL)

        assert LOGIN_URL in profile_page.get_current_url()

