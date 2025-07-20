from datetime import datetime
from typing import Sequence
from zoneinfo import ZoneInfo

import regex

from lxml import html
from selenium.common import NoSuchElementException
from sqlalchemy import select, Row
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import and_

from decorator import time_it
from database import get_session
from exceptions import InvalidSearchException
from log import CustomLogger
from selenium_browser import SeleniumBrowser
from model import Pesquisa, ServicoPesquisa, Lote


logger = CustomLogger().get_logger()


class SearchProcess:

    def __init__(self) -> None:
        self._session = get_session()

    def get_consultas(self, page: int, limit: int) -> Sequence[Row[tuple[Pesquisa]]]:
        statement = select(Pesquisa).join(ServicoPesquisa, Pesquisa.servico_pesquisa_id == ServicoPesquisa.id)
        statement = statement.join(Lote, Lote.id == ServicoPesquisa.lote_id)
        statement = statement.where(and_(Pesquisa.data_conclusao == None, ServicoPesquisa.resultado == None))
        statement = statement.limit(limit).offset(page * limit)
        return self._session.execute(statement).fetchall()

    def busca(self) -> None:
        for pesquisa in self.get_consultas(0, 100):
            try:
                pesquisa = self._session.merge(pesquisa[0])
                site = pesquisa.servico_pesquisa.web_site.url
                tipo = pesquisa.servico_pesquisa.tipo
                logger.info(f"Realizando pesquisa tipo {tipo} para site {site}")
                resultado = self.consulta_pesquisa(pesquisa, site, tipo)
                self.grava_consulta(pesquisa, resultado)
            except InvalidSearchException as e:
                logger.warning(e.msg)
            except Exception:
                logger.exception(f"Falha ao buscar pesquisa {pesquisa.id}")

    @time_it
    def consulta_pesquisa(self, pesquisa: Pesquisa, site: str, tipo: str) -> str:
        html_content = None
        if tipo == "documento" and pesquisa.cpf is None and pesquisa.rg is None:
            raise InvalidSearchException(f"Não existe cpf ou rg para pesquisa id {pesquisa.id}")
        if tipo == "documento" and pesquisa.cpf is not None:
            logger.info(f"Realizando pesquisa documento cpf {pesquisa.cpf} para site {site}")
            html_content = self.carrega_informacao(site, "documento", pesquisa.cpf)
        elif tipo == "documento" and pesquisa.cpf is None and pesquisa.rg is not None:
            logger.info(f"Realizando pesquisa documento cpf {pesquisa.rg} para site {site}")
            html_content = self.carrega_informacao(site, "documento", pesquisa.rg)
        elif tipo == "nome_parte":
            logger.info(f"Realizando pesquisa nome_parte {pesquisa.nome} para site {site}")
            html_content = self.carrega_informacao(site, "nome_parte", pesquisa.nome)
        return self.consta_processo(html_content)

    def grava_consulta(self, pesquisa: Pesquisa, resultado: str) -> None:
        try:
            pesquisa.servico_pesquisa.resultado = resultado
            logger.info(f"Inserindo resultado {resultado} de pesquisa id {pesquisa.id}")
            pesquisa.data_conclusao = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
            logger.info(f"Data da conclusao {pesquisa.data_conclusao}")
            self._session.add(pesquisa)
            self._session.commit()
        except DatabaseError as e:
            logger.exception(f"Não foi possivel gravar a consulta {pesquisa.id} com resultado {resultado}")

    # Esse método tem como função enquadrar a pesquisa de acordo com o resultado obtido na pesquisa como Nada Consta, Consta
    # Criminal e Consta Cível.
    @staticmethod
    def consta_processo(content: str) -> str:
        content = html.fromstring(content)
        mensagem = content.xpath("//td[@id='mensagemRetorno']/li/text()")
        nada_consta = 'Não existem informações disponíveis para os parâmetros informados.'
        if len(mensagem) and mensagem[0] == nada_consta:
            return "Nada consta"
        mensagem = content.xpath("//span[@id='contadorDeProcessos']/text()")
        if len(mensagem) and regex.search("\d+ Processos encontrados", mensagem[0].strip()):
            return mensagem[0].strip()
        raise ValueError

    @staticmethod
    def carrega_informacao(site, tipo_busca, value):
        try:
            selenium_browser = SeleniumBrowser()
            selenium_browser.browser.get(site)
            if tipo_busca == "documento":
                return selenium_browser.search("DOCPARTE", value)
            return selenium_browser.search("NMPARTE", value)
        except NoSuchElementException:
            logger.error("Elemento utilizado no parser não foi encontrado")
            raise
        except Exception:
            logger.exception("Houve um erro ao iniciar o SeleniumBrowser")
            raise

    def __del__(self) -> None:
        self._session.close()


if __name__ == '__main__':
    search = SearchProcess()
    search.busca()