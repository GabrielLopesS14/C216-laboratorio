# 💰 Finanças Pessoais

Sistema completo de **controle de finanças pessoais** desenvolvido como projeto final do lab.
A aplicação permite registrar receitas e despesas, organizá-las por contas, categorias e tags, e
acompanhar um resumo financeiro através de uma interface web.

Todo o projeto roda em containers, orquestrados via **Docker Compose**, com backend REST, frontend
web e banco de dados relacional.

---

## 🧱 Arquitetura

A aplicação é dividida em três serviços independentes, cada um em seu próprio container:

```
┌──────────────┐        HTTP        ┌──────────────┐        SQL         ┌──────────────┐
│   Frontend   │  ───────────────►  │   Backend    │  ───────────────►  │   Banco de   │
│   (Flask)    │   requisições API  │  (FastAPI)   │   SQLAlchemy ORM   │  dados (PG)  │
│   :3000      │  ◄───────────────  │   :8000      │  ◄───────────────  │   :5432      │
└──────────────┘      JSON          └──────────────┘                    └──────────────┘
```

- **Frontend (Flask):** renderiza as telas e **não acessa o banco diretamente** — ele apenas
  consome a API do backend via HTTP.
- **Backend (FastAPI):** expõe a API REST, aplica as regras de negócio e é o único que conversa
  com o banco.
- **Banco (PostgreSQL):** persiste os dados. As tabelas são criadas automaticamente pelo backend
  na primeira inicialização (via SQLAlchemy).

---

## 🛠️ Tecnologias

| Camada        | Tecnologia                       |
|---------------|----------------------------------|
| Backend       | Python · FastAPI · Uvicorn       |
| ORM           | SQLAlchemy                       |
| Validação     | Pydantic                         |
| Banco         | PostgreSQL                       |
| Frontend      | Python · Flask · Bootstrap       |
| Testes        | Pytest · TestClient              |
| Orquestração  | Docker · Docker Compose          |

---

## 🗂️ Modelo de Dados

O banco possui **5 tabelas** e contempla os dois tipos de relacionamento exigidos:

| Relacionamento | Onde acontece | Significado |
|----------------|---------------|-------------|
| **N : 1** | `transacoes` → `contas` | Muitas transações pertencem a uma conta |
| **N : 1** | `transacoes` → `categorias` | Muitas transações pertencem a uma categoria |
| **N : M** | `transacoes` ↔ `tags` | Uma transação tem várias tags e vice-versa (via tabela de junção `transacao_tags`) |

Tabelas:

- **contas** — onde o dinheiro fica (ex: Nubank, Carteira, Poupança)
- **categorias** — natureza da transação (ex: Alimentação, Salário, Transporte)
- **transacoes** — cada movimentação financeira (receita ou despesa)
- **tags** — etiquetas livres para marcar transações (ex: viagem, trabalho)
- **transacao_tags** — tabela de associação que materializa o relacionamento N:M

---

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose instalados.
- Portas **3000**, **8000** e **5432** livres na máquina.

### Passo a passo

1. Suba toda a aplicação com um único comando:

   ```bash
   docker compose up --build
   ```

2. Acesse no navegador:

   | Serviço | URL |
   |---------|-----|
   | 🖥️ Frontend (aplicação) | http://localhost:3000 |
   | ⚙️ API (backend) | http://localhost:8000 |
   | 📚 Documentação interativa (Swagger) | http://localhost:8000/docs |

3. Para encerrar:

   ```bash
   docker compose down
   ```

   Para encerrar **e apagar os dados** do banco:

   ```bash
   docker compose down -v
   ```

---

## 🔌 Endpoints da API

Base: `http://localhost:8000/api/v1`

A API implementa **CRUD completo** para todas as entidades, cobrindo os métodos `GET`, `POST`,
`PUT` e `DELETE`

### Contas

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`    | `/contas`        | Lista todas as contas |
| `GET`    | `/contas/{id}`   | Busca uma conta pelo ID |
| `POST`   | `/contas`        | Cria uma nova conta |
| `PUT`    | `/contas/{id}`   | Atualiza uma conta |
| `DELETE` | `/contas/{id}`   | Remove uma conta |

### Categorias

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`    | `/categorias`        | Lista todas as categorias |
| `GET`    | `/categorias/{id}`   | Busca uma categoria pelo ID |
| `POST`   | `/categorias`        | Cria uma nova categoria |
| `PUT`    | `/categorias/{id}`   | Atualiza uma categoria |
| `DELETE` | `/categorias/{id}`   | Remove uma categoria |

### Transações

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`    | `/transacoes`        | Lista todas as transações |
| `GET`    | `/transacoes/{id}`   | Busca uma transação pelo ID |
| `POST`   | `/transacoes`        | Cria uma nova transação (com contas, categoria e tags) |
| `PUT`    | `/transacoes/{id}`   | Atualiza uma transação |
| `DELETE` | `/transacoes/{id}`   | Remove uma transação |

### Tags

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`    | `/tags`        | Lista todas as tags |
| `GET`    | `/tags/{id}`   | Busca uma tag pelo ID |
| `POST`   | `/tags`        | Cria uma nova tag |
| `PUT`    | `/tags/{id}`   | Atualiza uma tag |
| `DELETE` | `/tags/{id}`   | Remove uma tag |

---

## 🖥️ Telas do Frontend

| Tela | Descrição |
|------|-----------|
| **Dashboard** | Resumo financeiro: saldo total, receitas, despesas e últimas transações |
| **Transações** | Listagem, cadastro, edição e exclusão de movimentações |
| **Contas** | Gerenciamento das contas |
| **Categorias** | Gerenciamento das categorias |
| **Relatórios** | Visão dos gastos agrupados por categoria |

---

## 🧪 Testes

Os testes automatizados validam a API usando o `TestClient` do FastAPI.

Para executá-los, com os containers no ar:

```bash
docker compose exec backend pytest -v
```

Os testes cobrem: criação de múltiplos registros, listagem, busca por ID, atualização e remoção
para as principais entidades.

---

## ✅ Boas Práticas Adotadas

- **Arquitetura em camadas** (rotas → serviços → modelos), separando responsabilidades.
- **Frontend desacoplado** do banco: comunica-se apenas pela API, facilitando manutenção.
- **Variáveis de ambiente** para configuração de conexões (sem credenciais "chumbadas" no código).
- **Versão do PostgreSQL fixada** (`postgres:16`) para builds reproduzíveis.
- **Healthcheck** no banco: o backend só inicia quando o PostgreSQL está pronto, evitando erros de conexão.
- **Middleware de logging**: cada requisição é registrada, facilitando a observação dos logs.
- **Validação de dados** com Pydantic, garantindo integridade das entradas da API.
- **`.gitignore`** para evitar o versionamento de arquivos desnecessários (`__pycache__`, `.env`).

---

## 👤 Autor

Gabriel Lopes Silva
