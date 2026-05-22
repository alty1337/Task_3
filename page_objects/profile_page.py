import allure

from locators.profile_page_locators import ProfilePageLocators
from page_objects.base_page import BasePage
from urls import ORDER_HISTORY_URL, PROFILE_URL


class ProfilePage(BasePage):
    @allure.step("Ждем открытия личного кабинета")
    def wait_for_open_profile(self):
        self.wait_for_url_contains(PROFILE_URL)

    @allure.step("Переходим в историю заказов")
    def click_order_history(self):
        self.click(ProfilePageLocators.ORDER_HISTORY_LINK)

    @allure.step("Ждем открытия истории заказов")
    def wait_for_open_order_history(self):
        self.wait_for_url_contains(ORDER_HISTORY_URL)

    @allure.step("Ждем появления заказа в истории")
    def wait_for_order_number_in_history(self, order_number):
        self.wait_for_visibility(ProfilePageLocators.order_number(order_number))

    @allure.step("Выходим из аккаунта")
    def logout(self):
        self.click(ProfilePageLocators.LOGOUT_BUTTON)
