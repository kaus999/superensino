# SuperEnsino - Teste

Destinado a teste da SuperEnsino

## Disponível dentro django admin:

* Cadastro de exercícios com respostas;
* Validação de cadastro com uma resposta correta selecionada;
* Listagem de exercícios;
* Acesso ao UserEstatistica que mostra o resumo geral de desempenho do usuário nas respostas.

## Disponível nas apis rest:

* Listagem de exercícios;
* Listagem de alternativas podendo filtrar pelo exercício;
* Listagem e resumo das respostas dadas pelos usuários, quantidade de acertos, erros, aproveitamento, total de
  exercícios, total de exercícios respondidos;
* Permitir responder a um exercício, informando uma resposta, não permitir refazer o exercício.

## Tecnologias utilizadas:

![Badge](https://img.shields.io/static/v1?label=python3&message=framework&color=red&style=for-the-badge&logo=PYTHON)

![Badge](https://img.shields.io/static/v1?label=django&message=framework&color=blue&style=for-the-badge&logo=DJANGO)

![Badge](https://img.shields.io/static/v1?label=sqlite&message=framework&color=orange&style=for-the-badge&logo=SQLITE)

![Badge](https://img.shields.io/static/v1?label=poetry&message=framework&color=green&style=for-the-badge&logo=POETRY)

![Badge](https://img.shields.io/static/v1?label=docker&message=framework&color=lightgray&style=for-the-badge&logo=DOCKER)


## Arquivo para importação do postman

[Postman](docs/superensino.postman_collection.json)

## Documentação da api rest

[Documentação da API Rest](https://documenter.getpostman.com/view/14915687/UVyn1JVj)

## Como executar localmente

### Requisitos

* Instalar o python - https://www.python.org/downloads/
* Instalar o poetry - https://python-poetry.org/docs/
* Instalar o docker (opcional) - https://docs.docker.com/engine/install/

### Configurando o projeto e inserindo elementos

* Instalando dependências - `$ poetry install`
* Iniciando o shell do virtualenv - `$ poetry shell`
* Executando as migrações do banco de dados - `$ python manage.py migrate`
* Criando super usuário no django - `$ python manage.py createsuperuser`
* Criando usuário no django admin - `http://127.0.0.1:8000/admin/auth/user/`
* Criando exercícios pelo django admin - `http://127.0.0.1:8000/admin/exercicio/exercicio/`
* Já poderá a partir deste momento, acessar via api rest, conforme link da documentação acima, contém arquivo do postman
  para facilitar

### Testes unitários

* Iniciando o shell do virtualenv - `$ poetry shell`
* Executando os testes - `$ python manage.py test`

### Deploy no Docker

* Gerar o arquivo requirements.txt - `$ poetry export -f requirements.txt --output requirements.txt`
* Build do Dockerfile - `$ docker build -t superensino-1.0.0 .`
* Executar o container - `$ docker run -dp 8000:8000 superensino-1.0.0`

**Observação**: verifique a versão antes de executar o deploy.

#### Parâmetros do Docker

* `DATABASE_URL` - Caminho e nome do arquivo sqlite.

#### Volume Docker

* `/app/api` - Diretório da aplicação.


