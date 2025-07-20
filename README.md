# Desafio Fidelity

## Para rodar a aplicação de forma dockerizada é necessário instalar.
* [docker](https://www.docker.com/get-started/)
* [docker-compose](https://docs.docker.com/compose/install/)
* make *verifique como realizar a instalação para seu sistema operacional*

### Realizando a instalação dos requisitos rode os commandos a seguir
```shell
make up-db
```
```shell
make migration
```
```shell
make seed
```
```shell
make crawler
```
### Para acompanhar os logs
```shell
make logs
```

## Para rodar a aplicação de forma nativa é necessário instalar
* [python3](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/)
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* [firefox](https://www.firefox.com/pt-BR/thanks/)
### rodar
```shell
python -m pip install -r requirements.txt
```
### É necessário ter uma instancia do *postgres* rodando para utilizar o projeto.
Abra o arquivo *alembic.ini* na linha 87 e altere os valores para os utilizados para conectar em sua base de dados.
```shell
python -m alembic upgrade head
```
Todo o projeto é parametrizavel a partir do arquivo *src/config.py* onde pode se utilizar de variaveis de ambiente para configurar conexão com o banco e o caminho para o geckodriver.

### Para rodar o projeto navegue até a pasta src e rode
```shell
python app.py
```