import allure

from locators.auth_locators import ResetPasswordPageLocators
from page_objects.base_page import BasePage


class ResetPasswordPage(BasePage):
    @allure.step("Вводим новый пароль")
    def fill_new_password(self, password):
        self.fill_input(ResetPasswordPageLocators.PASSWORD_INPUT, password)

    @allure.step("Нажимаем кнопку показать/скрыть пароль")
    def click_password_visibility_button(self):
        self.click(ResetPasswordPageLocators.PASSWORD_VISIBILITY_BUTTON)

    @allure.step("Проверяем активное поле пароля")
    def active_password_field_is_visible(self):
        return self.wait_for_visibility(ResetPasswordPageLocators.ACTIVE_PASSWORD_FIELD).is_displayed()

