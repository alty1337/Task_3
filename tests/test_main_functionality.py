import allure

from data import INGREDIENT_DETAILS_TITLE
from page_objects.feed_page import FeedPage
from page_objects.login_page import LoginPage
from page_objects.main_page import MainPage
from urls import BASE_URL, FEED_URL


@allure.suite("Основной функционал")
class TestMainFunctionality:
    @allure.title("Переход по клику на Конструктор")
    def test_click_constructor_opens_main_page(self, driver):
        feed_page = FeedPage(driver)
        main_page = MainPage(driver)

        feed_page.open()
        feed_page.click_constructor_link()
        main_page.wait_for_open_main_page()

        assert BASE_URL in main_page.get_current_url()

    @allure.title("Переход по клику на Лента заказов")
    def test_click_feed_opens_feed_page(self, driver):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        main_page.open()
        main_page.click_feed_link()
        feed_page.wait_for_open_feed()

        assert FEED_URL in feed_page.get_current_url()

    @allure.title("Клик на ингредиент открывает окно с деталями")
    def test_click_ingredient_opens_details_modal(self, driver):
        main_page = MainPage(driver)

        main_page.open()
        main_page.open_ingredient_details()
        main_page.wait_for_ingredient_details()

        assert main_page.get_ingredient_details_title() == INGREDIENT_DETAILS_TITLE

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_ingredient_details_modal(self, driver):
        main_page = MainPage(driver)

        main_page.open()
        main_page.open_ingredient_details()
        main_page.wait_for_ingredient_details()
        main_page.close_modal()

        assert main_page.is_ingredient_details_hidden()

    @allure.title("При добавлении ингредиента увеличивается каунтер")
    def test_add_ingredient_increases_counter(self, driver):
        main_page = MainPage(driver)

        main_page.open()
        counter_before = main_page.get_ingredient_counter()
        main_page.add_ingredient_to_constructor()
        counter_after = main_page.get_ingredient_counter()

        assert counter_after > counter_before

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_authorized_user_can_create_order(self, driver, user):
        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        login_page.open()
        login_page.login(user["email"], user["password"])
        main_page.wait_for_open_main_page()
        main_page.add_ingredient_to_constructor()
        main_page.click_order_button()

        assert main_page.get_order_number().isdigit()
