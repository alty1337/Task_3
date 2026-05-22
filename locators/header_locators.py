from selenium.webdriver.common.by import By


class HeaderLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    FEED_LINK = (By.XPATH, "//p[text()='Лента Заказов']/parent::a")
    ACCOUNT_LINK = (By.XPATH, "//p[text()='Личный Кабинет']/parent::a")

