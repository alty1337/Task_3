from selenium.webdriver.common.by import By


class MainPageLocators:
    INGREDIENT_CARD = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient')])[1]")
    INGREDIENT_COUNTER = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient_ingredient')]//p[contains(@class, 'counter_counter__num')])[1]",
    )
    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    INGREDIENT_DETAILS_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow')]")
    ORDER_SUCCESS_TEXT = (By.XPATH, "//p[text()='Ваш заказ начали готовить']")
    MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//button")

