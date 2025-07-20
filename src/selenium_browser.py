from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.select import Select

from config import Config
from log import CustomLogger


logger = CustomLogger().get_logger()


class SeleniumBrowser:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        service = Service(Config.EXECUTABLE_PATH)
        logger.info("Iniciando selenium browser")
        self._browser = webdriver.Firefox(service=service, options=options)

    @property
    def browser(self) -> webdriver.Firefox:
        return self._browser

    def search(self, value_element: str, value_search: str) -> str:
        try:
            logger.info(f"Buscando {value_search} com parametro {value_element}")
            element = self._browser.find_element('xpath', '//*[@id="cbPesquisa"]')
            Select(element).select_by_value(value_element)
            xpath = f'//*[@id="campo_{value_element}"]'
            self._browser.find_element('xpath', xpath).send_keys(value_search)
            if  value_element == 'NMPARTE':
                self._browser.find_element('xpath', "//span[@id='pesquisarPorNomeCompleto']").click()
            self._browser.find_element('xpath', '//*[@id="botaoConsultarProcessos"]').click()
            logger.info(f"Buscando {value_search} com sucesso")
            return self.browser.page_source
        except NoSuchElementException:
            raise

    def __del__(self):
        self._browser.quit()