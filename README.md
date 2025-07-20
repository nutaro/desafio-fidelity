## Desafio Fidelity

Para rodar a aplicação de forma dockerizada é necessário instalar.
* [docker](https://www.docker.com/get-started/)
* [docker-compose](https://docs.docker.com/compose/install/)
* make *verifique como realizar a instalação para seu sistema operacional*

Realizando a instalação dos requisitos rode os commandos a seguir
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