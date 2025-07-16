from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from config import Config


class SeleniumBrowser:

    def __init__(self):
        options = Options()
        service = Service(Config.EXECUTABLE_PATH)
        self._browser = webdriver.Firefox(service=service, options=options)

    @property
    def browser(self) -> webdriver.Firefox:
        return self._browser

    def search_by_nome_parte(self, value_element: str, value_search: str) -> str:
        try:
            element = self._browser.find_element('xpath', '//*[@id="cbPesquisa"]')
            Select(element).select_by_value(value_element)
            xpath = f'//*[@id="campo_{value_element}"]'
            self._browser.find_element('xpath', xpath).send_keys(value_search)
            self._browser.find_element('xpath', '//*[@id="botaoConsultarProcessos"]').click()
            return self.browser.page_source
        except NoSuchElementException:
            raise NoSuchElementException

    def __del__(self):
        self._browser.quit()