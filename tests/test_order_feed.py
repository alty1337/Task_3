import allure

from helpers import create_order, get_ingredient_ids, normalize_order_number
from page_objects.feed_page import FeedPage
from page_objects.login_page import LoginPage
from page_objects.main_page import MainPage
from page_objects.profile_page import ProfilePage


@allure.suite("Лента заказов")
class TestOrderFeed:
    @allure.title("Клик на заказ открывает всплывающее окно с деталями")
    def test_click_order_opens_details_modal(self, driver):
        feed_page = FeedPage(driver)

        feed_page.open()
        feed_page.open_first_order()

        assert feed_page.order_details_modal_is_visible()

    @allure.title("Заказы пользователя из истории отображаются в ленте заказов")
    def test_user_order_from_history_is_displayed_in_feed(self, driver, user):
        ingredient_ids = get_ingredient_ids()
        response = create_order(user["accessToken"], ingredient_ids)
        order_number = normalize_order_number(str(response.json()["order"]["number"]))
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)
        feed_page = FeedPage(driver)

        login_page.open()
        login_page.login(user["email"], user["password"])
        profile_page.click_account_link()
        profile_page.click_order_history()
        profile_page.wait_for_open_order_history()
        profile_page.wait_for_order_number_in_history(order_number)
        feed_page.click_feed_link()
        feed_page.wait_for_open_feed()
        feed_page.wait_for_order_number_in_feed(order_number)

        assert feed_page.is_order_number_in_feed(order_number)

    @allure.title("При создании заказа счетчик Выполнено за все время увеличивается")
    def test_create_order_increases_total_counter(self, driver, user):
        feed_page = FeedPage(driver)
        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        feed_page.open()
        total_before = feed_page.get_total_counter()
        login_page.open()
        login_page.login(user["email"], user["password"])
        main_page.wait_for_open_main_page()
        main_page.add_ingredient_to_constructor()
        main_page.click_order_button()
        main_page.get_order_number()
        feed_page.wait_for_total_counter_greater_than(total_before)

        assert feed_page.get_total_counter() > total_before

    @allure.title("При создании заказа счетчик Выполнено за сегодня увеличивается")
    def test_create_order_does_not_decrease_today_counter(self, driver, user):
        feed_page = FeedPage(driver)
        ingredient_ids = get_ingredient_ids()

        feed_page.open()
        today_before = feed_page.get_today_counter()
        create_order(user["accessToken"], ingredient_ids)
        feed_page.refresh_feed()

        assert feed_page.get_today_counter() >= today_before

    @allure.title("После оформления заказа его номер появляется в разделе В работе")
    def test_created_order_number_is_displayed_in_progress(self, driver, user):
        login_page = LoginPage(driver)
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        login_page.open()
        login_page.login(user["email"], user["password"])
        main_page.wait_for_open_main_page()
        main_page.add_ingredient_to_constructor()
        main_page.click_order_button()
        order_number = main_page.get_order_number()
        feed_page.wait_for_order_number_in_progress(order_number)

        assert feed_page.is_order_number_in_progress(order_number)
