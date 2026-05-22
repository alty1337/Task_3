from selenium.webdriver.common.by import By


class CommonLocators:
    MODAL_OVERLAY = (By.XPATH, "//*[contains(@class, 'Modal_modal_overlay')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//*[contains(@class, 'Modal_modal')]//button")
