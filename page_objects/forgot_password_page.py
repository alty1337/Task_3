import allure

from locators.auth_locators import ForgotPasswordPageLocators
from page_objects.base_page import BasePage
from urls import FORGOT_PASSWORD_URL


class ForgotPasswordPage(BasePage):
    @allure.step("Открываем страницу восстановления пароля")
    def open(self):
        self.open_page(FORGOT_PASSWORD_URL)

    @allure.step("Вводим email и нажимаем Восстановить")
    def restore_password(self, email):
        self.fill_input(ForgotPasswordPageLocators.EMAIL_INPUT, email)
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)

