from selenium.webdriver.common.by import By

from helpers import order_number_variants


class ProfilePageLocators:
    ORDER_HISTORY_LINK = (By.XPATH, "//a[text()='История заказов']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")

    @staticmethod
    def order_number(order_number):
        variants = order_number_variants(order_number)
        conditions = " or ".join(f"contains(text(), '{variant}')" for variant in variants)
        return By.XPATH, f"//*[{conditions}]"
