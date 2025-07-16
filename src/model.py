from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Website(Base):

    __tablename__ = 'web_site'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(), unique=False)
    url: Mapped[String] = mapped_column(String(), unique=False)


class Funcionario(Base):

    __tablename__ = 'funcionario'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[String] = mapped_column(String(), unique=True)


class Fornecedor(Base):

    __tablename__ = 'fornecedor'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_id: Mapped[Integer] = mapped_column(ForeignKey('estado.id'))
    nome: Mapped[String] = mapped_column(String(), unique=True)


class Estado(Base):

    __tablename__ = 'estado'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uf: Mapped[String] = mapped_column(String(2), unique=True)
    nome: Mapped[String] = mapped_column(String(), unique=True)


class Lote(Base):

    __tablename__ = 'lote'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey('funcionario.id'), nullable=False)
    prazo: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tipo: Mapped[String] = mapped_column(String, nullable=False)
    prioridade: Mapped[int] = mapped_column(Integer, nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LotePesquisa(Base):

    __tablename__ = 'lote_pesquisa'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lote_id: Mapped[int] = mapped_column(ForeignKey('lote.id'))
    pesquisa_id: Mapped[int] = mapped_column(ForeignKey('pesquisa.id'))
    fornecedor_id: Mapped[int] = mapped_column(ForeignKey('fornecedor.id'))
    estado_id: Mapped[int] = mapped_column(ForeignKey('estado.id'))
    conclusao: Mapped[String] = mapped_column(String(), nullable=True)
    observacao: Mapped[String] = mapped_column(String(), nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    data_conclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ServicoPesquisa(Base):

    __tablename__ = 'servico_pesquisa'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    web_site_id: Mapped[int] = mapped_column(ForeignKey('web_site.id'))
    tipo: Mapped[String] = mapped_column(String(), nullable=False)
    servico: Mapped[String] = mapped_column(String(), nullable=False)
    resultado: Mapped[String] = mapped_column(String(), nullable=False)


class Pesquisa(Base):

    __tablename__ = 'pesquisa'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    servico_pesquisa_id: Mapped[int] = mapped_column(ForeignKey('servico_pesquisa.id'))
    nome: Mapped[String] = mapped_column(String(), nullable=False)
    cpf: Mapped[String] = mapped_column(String(11), nullable=False)
    rg: Mapped[String] = mapped_column(String, nullable=True)
    uf_rg: Mapped[String] = mapped_column(String(2), nullable=True)
    nascimento: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    uf_nascimento: Mapped[String] = mapped_column(String(2), nullable=False)
    nome_mae: Mapped[String] = mapped_column(String(), nullable=False)
    data_entrada: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_conclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    anexo: Mapped[String] = mapped_column(String(), nullable=True)