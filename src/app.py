from typing import Sequence

import regex

from lxml import html
from sqlalchemy import select, Row
from sqlalchemy.sql import and_

from database import get_session
from selenium_browser import SeleniumBrowser
from model import Pesquisa, ServicoPesquisa, Lote


class SearchProcess:

    def __init__(self) -> None:
        self._session = get_session()

    def get_consultas(self) -> Sequence[Row[tuple[Pesquisa]]]:
        statement = select(Pesquisa).join(ServicoPesquisa, Pesquisa.servico_pesquisa_id == ServicoPesquisa.id)
        statement = statement.join(Lote, Lote.id == ServicoPesquisa.lote_id)
        statement = statement.where(and_(Pesquisa.data_conclusao == None, ServicoPesquisa.resultado == None))
        return self._session.execute(statement).fetchall()

    # Esse método possui a função de consultar a pesquisa no banco de dados e executá-la utilizando a biblioteca Selenoid.
    # A parte da execução é aplicada utilizando o método executaPesquisa().
    def search(self) -> None:
        for pesquisa in self.get_consultas():
            pesquisa = self._session.merge(pesquisa[0])
            site = pesquisa.servico_pesquisa.web_site.url
            tipo = pesquisa.servico_pesquisa.tipo
            resultado = None
            if tipo == "documento" and pesquisa.cpf is None and pesquisa.rg is None:
                raise ValueError
            if tipo == "documento" and pesquisa.cpf is not None:
                resultado = self.load_info(site, "documento", pesquisa.cpf)
            elif tipo == "documento" and pesquisa.cpf is None and pesquisa.rg is not None:
                resultado = self.load_info(site, "documento", pesquisa.rg)
            elif tipo == "nome_parte":
                resultado = self.load_info(site, "nome_parte", pesquisa.nome)
            consta = self.consta_processo(resultado)


    # Esse método tem como função enquadrar a pesquisa de acordo com o resultado obtido na pesquisa como Nada Consta, Consta
    # Criminal e Consta Cível.
    @staticmethod
    def consta_processo(content: str) -> str:
        content = html.fromstring(content)
        mensagem = content.xpath("//td[ @ id = 'mensagemRetorno']/li/text()")
        nada_consta = 'Não existem informações disponíveis para os parâmetros informados.'
        if len(mensagem) and mensagem[0] == nada_consta:
            return "Nada consta"
        mensagem = content.xpath("//span[@id='contadorDeProcessos']/text()")
        if len(mensagem) and regex.search("\d+ Processos encontrados", mensagem[0].strip()):
            return mensagem[0].strip()

    @staticmethod
    def load_info(site, tipo_busca, value):
        selenium_browser = SeleniumBrowser()
        selenium_browser.browser.get(site)

        if tipo_busca == "documento":
            return selenium_browser.search("DOCPARTE", value)
        return selenium_browser.search("NMPARTE", value)


if __name__ == '__main__':
    search = SearchProcess()
    search.search()