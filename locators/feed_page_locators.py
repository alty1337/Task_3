from selenium.webdriver.common.by import By

from helpers import normalize_order_number, order_number_variants


class FeedPageLocators:
    ORDER_CARD = (
        By.XPATH,
        "(//a[contains(@href, '/feed/') and contains(@href, '/feed/6')])[1]",
    )
    FIRST_ORDER_NUMBER = (By.XPATH, "(//p[contains(text(), '#')])[1]")
    TOTAL_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_LIST = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderList__') and not(contains(@class, 'Ready'))]",
    )

    @staticmethod
    def order_number(order_number):
        variants = order_number_variants(order_number)
        conditions = " or ".join(f"contains(text(), '{variant}')" for variant in variants)
        return By.XPATH, f"//*[{conditions}]"

    @staticmethod
    def order_number_in_progress(order_number):
        normalized = normalize_order_number(order_number)
        padded5 = normalized.zfill(5)
        return (
            By.XPATH,
            "//ul[contains(@class, 'OrderFeed_orderList__') and not(contains(@class, 'Ready'))]"
            f"//li[normalize-space()='{padded5}' or normalize-space()='{normalized}']",
        )
