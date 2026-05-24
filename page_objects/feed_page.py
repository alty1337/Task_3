import allure

from helpers import normalize_order_number
from locators.feed_page_locators import FeedPageLocators
from page_objects.base_page import BasePage
from urls import FEED_URL


class FeedPage(BasePage):
    @allure.step("Открываем ленту заказов")
    def open(self):
        self.open_page(FEED_URL)
        self.wait_for_feed_loaded()

    @allure.step("Ждем загрузки ленты заказов")
    def wait_for_feed_loaded(self):
        self.wait_for_visibility(FeedPageLocators.TOTAL_COUNTER)
        self.wait_for_visibility(FeedPageLocators.ORDER_CARD)

    @allure.step("РћР±РЅРѕРІР»СЏРµРј Р»РµРЅС‚Сѓ Р·Р°РєР°Р·РѕРІ")
    def refresh_feed(self):
        self.refresh_page()
        self.wait_for_feed_loaded()

    @allure.step("Открываем первый заказ в ленте")
    def open_first_order(self):
        self.wait_for_feed_loaded()
        self.click(FeedPageLocators.ORDER_CARD)

    @allure.step("Получаем номер последнего заказа в ленте")
    def get_latest_order_number(self):
        order_text = self.get_text(FeedPageLocators.FIRST_ORDER_NUMBER)
        return normalize_order_number(order_text.replace("#", ""))

    @allure.step("Проверяем, что открыты детали заказа")
    def order_details_modal_is_visible(self):
        self.wait_for_url_path_suffix_longer_than("/feed/", 20)
        return "/feed/" in self.get_current_url()

    @allure.step("Получаем счетчик Выполнено за все время")
    def get_total_counter(self):
        return int(self.get_text(FeedPageLocators.TOTAL_COUNTER))

    @allure.step("Получаем счетчик Выполнено за сегодня")
    def get_today_counter(self):
        return int(self.get_text(FeedPageLocators.TODAY_COUNTER))

    @allure.step("Ждем открытия ленты заказов")
    def wait_for_open_feed(self):
        self.wait_for_url_contains(FEED_URL)
        self.wait_for_feed_loaded()

    @allure.step("Ждем увеличения счетчика Выполнено за все время")
    def wait_for_total_counter_greater_than(self, value):
        self.wait_for_element_text_number_greater_than(FeedPageLocators.TOTAL_COUNTER, value)

    @allure.step("Ждем увеличения счетчика Выполнено за сегодня")
    def wait_for_today_counter_greater_than(self, value):
        self.wait_for_element_text_number_greater_than(FeedPageLocators.TODAY_COUNTER, value)

    @allure.step("Ждем появления заказа в ленте")
    def wait_for_order_number_in_feed(self, order_number):
        self.wait_for_visibility(FeedPageLocators.order_number(order_number))

    @allure.step("Проверяем, что номер заказа отображается в ленте")
    def is_order_number_in_feed(self, order_number):
        return self.wait_for_visibility(FeedPageLocators.order_number(order_number)).is_displayed()

    @allure.step("Ждем появления заказа в блоке В работе")
    def wait_for_order_number_in_progress(self, order_number):
        self.wait_for_visibility(FeedPageLocators.IN_PROGRESS_LIST)
        self.wait_for_element_exists(
            FeedPageLocators.order_number_in_progress(order_number),
            message=f"Заказ {order_number} не появился в разделе В работе",
        )

    @allure.step("Проверяем, что номер заказа отображается в блоке В работе")
    def is_order_number_in_progress(self, order_number):
        return self._is_order_number_in_progress(order_number)

    def _is_order_number_in_progress(self, order_number):
        return self.element_exists(FeedPageLocators.order_number_in_progress(order_number))
