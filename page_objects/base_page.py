from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from locators.common_locators import CommonLocators
from locators.header_locators import HeaderLocators


class UrlPathSuffixLongerThan:
    def __init__(self, path, min_length):
        self.path = path
        self.min_length = min_length

    def __call__(self, driver):
        return self.path in driver.current_url and len(driver.current_url.split(self.path)[-1]) > self.min_length


class ElementTextNumberGreaterThan:
    def __init__(self, page, locator, value):
        self.page = page
        self.locator = locator
        self.value = value

    def __call__(self, driver):
        elements = self.page.find_elements(self.locator)
        if not elements or not elements[0].text:
            return False
        return int(elements[0].text) > self.value


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_page(self, url):
        self.driver.get(url)
        self.close_modal_if_present()

    def go_to_url(self, url):
        self.driver.get(url)

    def refresh_page(self):
        self.driver.refresh()

    def close_modal_if_present(self):
        short_wait = WebDriverWait(self.driver, 3)
        try:
            short_wait.until(expected_conditions.visibility_of_element_located(CommonLocators.MODAL_OVERLAY))
            close_button = self.driver.find_element(*CommonLocators.MODAL_CLOSE_BUTTON)
            try:
                close_button.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", close_button)
            self.wait.until(expected_conditions.invisibility_of_element_located(CommonLocators.MODAL_OVERLAY))
        except TimeoutException:
            pass

    def wait_for_visibility(self, locator):
        return self.wait.until(expected_conditions.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(expected_conditions.element_to_be_clickable(locator))

    def wait_for_invisibility(self, locator):
        self.wait.until(expected_conditions.invisibility_of_element_located(locator))

    def wait_for_url_contains(self, text):
        self.wait.until(expected_conditions.url_contains(text))

    def wait_for_url_to_be(self, url):
        self.wait.until(expected_conditions.url_to_be(url))

    def wait_for_url_path_suffix_longer_than(self, path, min_length):
        self.wait.until(UrlPathSuffixLongerThan(path, min_length))

    def wait_for_element_text_number_greater_than(self, locator, value):
        for _ in range(2):
            try:
                return self.wait.until(ElementTextNumberGreaterThan(self, locator, value))
            except TimeoutException:
                self.refresh_page()
        return self.wait.until(ElementTextNumberGreaterThan(self, locator, value))

    def wait_until(self, condition, message=None):
        return self.wait.until(condition, message=message)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def element_exists(self, locator):
        return bool(self.find_elements(locator))

    def wait_for_element_exists(self, locator, message=None):
        return self.wait.until(expected_conditions.presence_of_element_located(locator), message=message)

    def click(self, locator):
        self.close_modal_if_present()
        element = self.wait_for_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.close_modal_if_present()
            element = self.wait_for_clickable(locator)
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

    def fill_input(self, locator, text):
        self.close_modal_if_present()
        element = self.wait_for_visibility(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait_for_visibility(locator).text

    def get_current_url(self):
        return self.driver.current_url

    def drag_and_drop(self, source_locator, target_locator):
        self.close_modal_if_present()
        source = self.wait_for_visibility(source_locator)
        target = self.wait_for_visibility(target_locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[1].scrollIntoView({block: 'center'});",
            source,
            target,
        )

        if self._is_firefox():
            self._drag_and_drop_in_firefox(source, target)
            return

        try:
            ActionChains(self.driver).drag_and_drop(source, target).perform()
        except Exception:
            self._drag_and_drop_with_js(source, target)

    def _is_firefox(self):
        return self.driver.name == "firefox"

    def _drag_and_drop_in_firefox(self, source, target):
        try:
            self._drag_and_drop_with_js(source, target)
            return
        except Exception:
            pass

        mouse = PointerInput(interaction.POINTER_MOUSE, "mouse")
        actions = ActionBuilder(self.driver, mouse=mouse)
        actions.pointer_action.move_to(source).pointer_down().pause(0.3).move_to(target).pause(0.3).pointer_up()
        actions.perform()

    def _drag_and_drop_with_js(self, source, target):
        self.driver.execute_script(
            """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();

            source.dispatchEvent(
                new DragEvent('dragstart', { bubbles: true, cancelable: true, dataTransfer }),
            );
            target.dispatchEvent(
                new DragEvent('dragenter', { bubbles: true, cancelable: true, dataTransfer }),
            );
            target.dispatchEvent(
                new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer }),
            );
            target.dispatchEvent(
                new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer }),
            );
            source.dispatchEvent(
                new DragEvent('dragend', { bubbles: true, cancelable: true, dataTransfer }),
            );
            """,
            source,
            target,
        )

    def click_constructor_link(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)

    def click_feed_link(self):
        self.click(HeaderLocators.FEED_LINK)

    def click_account_link(self):
        self.click(HeaderLocators.ACCOUNT_LINK)
