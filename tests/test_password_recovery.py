import allure

from data import RESET_PASSWORD
from page_objects.forgot_password_page import ForgotPasswordPage
from page_objects.login_page import LoginPage
from page_objects.reset_password_page import ResetPasswordPage
from urls import FORGOT_PASSWORD_URL, RESET_PASSWORD_URL


@allure.suite("Восстановление пароля")
class TestPasswordRecovery:
    @allure.title("Переход на страницу восстановления пароля")
    def test_click_forgot_password_opens_recovery_page(self, driver):
        login_page = LoginPage(driver)

        login_page.open()
        login_page.click_forgot_password()
        login_page.wait_for_url_contains(FORGOT_PASSWORD_URL)

        assert FORGOT_PASSWORD_URL in login_page.get_current_url()

    @allure.title("Ввод почты и клик по кнопке Восстановить")
    def test_restore_password_opens_reset_page(self, driver, user):
        forgot_password_page = ForgotPasswordPage(driver)

        forgot_password_page.open()
        forgot_password_page.restore_password(user["email"])
        forgot_password_page.wait_for_url_contains(RESET_PASSWORD_URL)

        assert RESET_PASSWORD_URL in forgot_password_page.get_current_url()

    @allure.title("Клик по кнопке показать пароль делает поле активным")
    def test_click_password_visibility_button_makes_password_field_active(self, driver, user):
        forgot_password_page = ForgotPasswordPage(driver)
        reset_password_page = ResetPasswordPage(driver)

        forgot_password_page.open()
        forgot_password_page.restore_password(user["email"])
        reset_password_page.fill_new_password(RESET_PASSWORD)
        reset_password_page.click_password_visibility_button()

        assert reset_password_page.active_password_field_is_visible()

