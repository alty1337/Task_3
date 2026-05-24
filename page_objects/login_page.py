import allure

from locators.auth_locators import LoginPageLocators
from page_objects.base_page import BasePage
from urls import LOGIN_URL


class LoginPage(BasePage):
    @allure.step("Открываем страницу логина")
    def open(self):
        self.open_page(LOGIN_URL)

    @allure.step("Переходим к восстановлению пароля")
    def click_forgot_password(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    @allure.step("Логинимся пользователем")
    def login(self, email, password):
        self.fill_input(LoginPageLocators.EMAIL_INPUT, email)
        self.fill_input(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)

