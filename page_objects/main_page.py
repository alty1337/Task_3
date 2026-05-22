import allure
from selenium.common.exceptions import TimeoutException

from helpers import normalize_order_number
from locators.feed_page_locators import FeedPageLocators
from locators.main_page_locators import MainPageLocators
from page_objects.base_page import BasePage
from urls import BASE_URL, FEED_URL, MAIN_PAGE_URL


class MainPage(BasePage):
    @allure.step("Открываем главную страницу")
    def open(self):
        self.open_page(BASE_URL)

    @allure.step("Открываем карточку ингредиента")
    def open_ingredient_details(self):
        self.click(MainPageLocators.INGREDIENT_CARD)

    @allure.step("Получаем значение каунтера ингредиента")
    def get_ingredient_counter(self):
        counters = self.driver.find_elements(*MainPageLocators.INGREDIENT_COUNTER)
        return int(counters[0].text) if counters else 0

    @allure.step("Добавляем ингредиент в конструктор")
    def add_ingredient_to_constructor(self):
        counter_before = self.get_ingredient_counter()
        self.drag_and_drop(MainPageLocators.INGREDIENT_CARD, MainPageLocators.CONSTRUCTOR_DROP_AREA)
        self.wait.until(lambda driver: self.get_ingredient_counter() > counter_before)

    @allure.step("Оформляем заказ")
    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Закрываем модальное окно")
    def close_modal(self):
        self.close_modal_if_present()
        for button in self.driver.find_elements(*MainPageLocators.MODAL_CLOSE_BUTTON):
            if button.is_displayed():
                button.click()
                break
        self.wait_for_invisibility(MainPageLocators.INGREDIENT_DETAILS_TITLE)

    @allure.step("Проверяем, что детали ингредиента скрыты")
    def is_ingredient_details_hidden(self):
        try:
            self.wait_for_invisibility(MainPageLocators.INGREDIENT_DETAILS_TITLE)
            return True
        except TimeoutException:
            return False

    @allure.step("Ждем подтверждения создания заказа")
    def wait_for_order_success(self):
        self.wait_for_visibility(MainPageLocators.ORDER_SUCCESS_TEXT)

    @allure.step("Получаем номер созданного заказа")
    def get_order_number(self):
        self.wait_for_order_success()
        self.driver.get(FEED_URL)
        self.wait_for_visibility(FeedPageLocators.TOTAL_COUNTER)
        self.wait_for_visibility(FeedPageLocators.ORDER_CARD)
        order_text = self.get_text(FeedPageLocators.FIRST_ORDER_NUMBER)
        return normalize_order_number(order_text.replace("#", ""))

    @allure.step("Ждем открытия главной страницы")
    def wait_for_open_main_page(self):
        self.wait_for_url_to_be(MAIN_PAGE_URL)

    @allure.step("Ждем открытия деталей ингредиента")
    def wait_for_ingredient_details(self):
        self.wait_for_visibility(MainPageLocators.INGREDIENT_DETAILS_TITLE)

    @allure.step("Получаем заголовок деталей ингредиента")
    def get_ingredient_details_title(self):
        return self.get_text(MainPageLocators.INGREDIENT_DETAILS_TITLE)
