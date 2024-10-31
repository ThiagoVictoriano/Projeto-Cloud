# Projeto-Cloud

Thiago Torres Victoriano

# Documentação do Projeto

## Visão Geral

Este projeto é projeto construído com FastAPI e SQLModel. O sistema permite que os usuários se registrem, façam login e recebam informações relativas às principais cryptocurrencies por meio da API externa da coingecko. As funcionalidades incluem:

- Cadastro e autenticação de usuários
- Acesso às informações das principais criptomoedas

### Pré-requisitos
---
Antes de instalar e executar o projeto, você precisa ter os seguintes itens instalados em seu sistema:

- **Docker**: Para criar e gerenciar containers. Você pode baixar o Docker [aqui](https://www.docker.com/get-started).
- **Docker Compose**: Para facilitar a orquestração de múltiplos containers.

## Tecnologias Utilizadas

- **Backend**: FastAPI
- **Banco de Dados**: MySQL
- **ORM**: SQLModel
- **Autenticação**: JWT
- **Docker**: Para containerização
- **Python**: 3.10

# Docker Hub

Link para o repositório: [thiagovic/projeto](https://hub.docker.com/repository/docker/thiagovic/projeto/general)

## Comandos Utilizados

```bash
docker login
docker tag mysql:5.7 thiagovic/projeto:latest
docker push thiagovic/projeto:latest
```

## Arquivo yaml

O arquivo compose.yaml se encontra na raiz do repositório, na mesma localização que o README.md, baixe-o ou simplesmente crie um arquivo próprio compose.yaml com o seguinte código:
```bash
name: projeto

services:
  web:
    image: thiagovic/projeto:latest
    ports:
      - "8000:8000"
    environment:
      MYSQL_USER: ${MYSQL_USER:-root}    
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-root} 
      MYSQL_HOST: ${MYSQL_HOST:-db:3306}
      MYSQL_DB: ${MYSQL_DB:-projeto} 
    restart: always
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD:-root}
      MYSQL_DATABASE: ${MYSQL_DB:-projeto}

    ports:
      - "3307:3306"
```

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone <URL do repositório>
   cd <nome do repositório>
   ```

2. **Construa e inicie os containers**:
   ```bash
   docker-compose up
   ```

3. **Acesse a aplicação** em `http://localhost:8000`.

## Uso

Após iniciar a aplicação, você pode usar os seguintes endpoints da API:

## Endpoints

### 1. Registro de Usuário

- **Método:** `POST`
- **Endpoint:** `/register`
- **Descrição:** Registra um novo usuário no sistema.
- **Corpo da Requisição:**
  ```json
  {
    "nome":  "string",
    "email": "string",
    "senha": "string"
  }
  ```
- **Resposta:**
  - **200 OK**: Retorna um token JWT.
  - **400 Bad Request**: Dados inválidos.

### 2. Login

- **Método:** `POST`
- **Endpoint:** `/login`
- **Descrição:** Autentica um usuário e retorna um token JWT.
- **Corpo da Requisição:**
  ```json
  {
    "email": "string",
    "senha": "string"
  }
  ```
- **Resposta:**
  - **200 OK**: Retorna um token JWT.
  - **401 Unauthorized**: Credenciais inválidas.

### 3. Consultar Api Externa

- **Método:** `GET`
- **Endpoint:** `/consultar`
- **Descrição:** Retorna uma lista de informações das principais cripto moedas.
- **Cabeçalho:**
  - `Authorization: Bearer {token}`
- **Resposta:**
  - **200 OK**: Retorna uma lista de dados.
  - **401 Unauthorized**: Token inválido ou não fornecido.

## Exemplo de Uso com cURL

### Register

```bash
curl -X POST http://localhost:8000/register \
     -H "Content-Type: application/json" \
     -d '{"nome": "teste", "email": "teste@email.com", "senha": "teste"}'
```

![register](img/endpoint_register.png)

### Login

```bash
curl -X POST http://localhost:8000/login \
     -H "Content-Type: application/json" \
     -d '{"email": "teste@email.com", "senha": "teste"}'
```

![login](img/endpoint_login.png)

### Requisição com Header de Autorização

Após o login, você deve incluir o token JWT nas requisições para endpoints protegidos:

```bash
curl -X GET http://localhost:8000/consultar \
     -H "Authorization: Bearer <seu_token_jwt>"
```

![consultar](img/endpoint_consultar.png)

### Video demonstrando as end points 📺
---
https://youtu.be/bvK75yAwn78?feature=shared