# 🚀 LLM Gateway API

A modern, scalable backend service built with **Python** and **FastAPI** for interacting with Large Language Models (LLMs).

Este projeto é um serviço backend moderno e escalável desenvolvido com **Python** e **FastAPI** para integração com Modelos de Linguagem de Larga Escala (LLMs).

---

## ✨ Features | Funcionalidades

- 🔌 **Pluggable LLM Providers**  
  Easily switch between providers (OpenAI, Ollama, etc.)  
  Fácil troca entre provedores (OpenAI, Ollama, etc.)

- 🧱 **Clean Architecture**  
  Clear separation of concerns across layers  
  Separação clara de responsabilidades entre camadas

- 🧠 **LLM Integration Layer**  
  Abstracted interface for provider independence  
  Interface abstrata para independência de provedores

- 📄 **Automatic API Documentation**  
  Swagger UI and ReDoc included  
  Documentação automática com Swagger e ReDoc

- ⚙️ **Environment-Based Configuration**  
  Secure configuration using environment variables  
  Configuração segura via variáveis de ambiente

- 🧾 **Structured Logging**  
  Centralized logging with Loguru  
  Logging estruturado com Loguru

- 📚 **Request History (In-Memory)**  
  Interaction tracking for debugging  
  Histórico de requisições em memória

- 🛡️ **Error Handling**  
  Centralized exception handling  
  Tratamento centralizado de erros

---

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- Pydantic v2
- HTTPX
- OpenAI SDK
- Loguru
- python-dotenv

---

## 📂 Project Structure | Estrutura do Projeto

```
app/
├── main.py                # Entry point / Ponto de entrada
├── core/                  # Configs e exceções
├── api/                   # Rotas / Controllers
├── schemas/               # Validação (Pydantic)
├── services/              # Regras de negócio
├── clients/               # Integrações externas (LLMs)
└── models/                # Modelos de domínio

.env.example
requirements.txt
README.md
```

---

## ⚙️ Running Locally | Executando Localmente

### Requirements | Requisitos

- Python 3.10+
- pip

### Setup

```bash
git clone <your-repo-url>
cd llm-gateway-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables | Variáveis de Ambiente

```bash
cp .env.example .env
```

Configure suas credenciais (ex: OpenAI API Key).

### Run the Application | Executar

```bash
uvicorn app.main:app --reload
```

API disponível em:

```
http://localhost:8000
```

---

## 📖 API Documentation | Documentação

- Swagger: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

---

## 🔌 Endpoints

### ➤ Health Check

```
GET /api/v1/health
```

### ➤ Send Prompt | Enviar Prompt

```
POST /api/v1/prompt
```

#### Body

```json
{
  "prompt": "What are the advantages of FastAPI?",
  "temperature": 0.7,
  "max_tokens": 200
}
```

### ➤ History | Histórico

```
GET /api/v1/history?limit=5
```

---

## 🧪 Example | Exemplo

```bash
curl -X POST "http://localhost:8000/api/v1/prompt" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Explain FastAPI benefits",
  "temperature": 0.7,
  "max_tokens": 200
}'
```

---

## 🧩 Architecture | Arquitetura

This project follows **Clean Architecture** and **SOLID principles**:

- Separation of concerns  
- Dependency inversion  
- High cohesion, low coupling  
- Easy extensibility  
- Testability  

Este projeto segue **Clean Architecture** e princípios **SOLID**:

- Separação de responsabilidades  
- Inversão de dependência  
- Baixo acoplamento  
- Alta coesão  
- Facilidade de testes  

---

## 🔄 LLM Providers

- `LLMClient` (interface base)
- `OpenAIClient`
- `OllamaClient`

Allows easy provider switching via configuration.

Permite trocar o provedor facilmente via configuração.

---

## 🚀 Roadmap

- [ ] PostgreSQL + SQLAlchemy/SQLModel  
- [ ] Authentication (JWT / OAuth2)  
- [ ] Streaming (SSE / WebSockets)  
- [ ] Tests with Pytest  
- [ ] Docker support  
- [ ] Rate limiting & caching  

---

## 📄 License

MIT License