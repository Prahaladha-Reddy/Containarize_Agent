# Email Managemsnt MultiAgent System

An AI-powered, fully containerized microservice stack that combines **FastAPI**, **LangGraph**, **SQLModel**, **PostgreSQL**, and a self-hosted **Gemma 3 model**. It orchestrates intelligent agents to perform research, generate content, and handle email automation—all with a single `docker compose up`.

---

## Key Features

### Supervisor-Agent Architecture using LangGraph

* A **Supervisor Agent** is created using `create_supervisor` from LangGraph.

* It coordinates two specialized **React-style Agents** (built with `create_react_agent`) with tool-specific roles:

  * **Research Agent 1**: Specialized in web search and summarization.
  * **Research Agent 2**: Specialized in content composition and drafting emails.

* The Supervisor dynamically routes sub-tasks to each Research Agent based on their tool access and strengths.

### Tool-Based Specialization

Each Research Agent is equipped with distinct tools. For example:

* Research Agent 1 may include tools like:

  * Web search
  * Text summarization
* Research Agent 2 may include tools like:

  * Email drafting
  * Explanation or paraphrasing tools

This tool-based specialization ensures modularity, fine-grained routing, and intelligent orchestration by the Supervisor Agent.

### Gemma 3 LLM via OpenAI-Compatible API

* A local **Gemma 3 model** is launched using the latest **Docker-based OpenAI-compatible runner**.
* This allows using open-source LLMs in place of OpenAI models while maintaining API compatibility.

### Secure Email Automation

* Uses `smtplib` for sending emails and `imaplib` for reading from the inbox.
* Compatible with **Gmail via Google App Passwords**.
* Requires enabling **2-Step Verification** on the Google account for secure access.

### SQLModel and PostgreSQL Integration

* Database: **PostgreSQL 17** (Docker container)
* ORM: **SQLModel** for clean, Pydantic-based schema modeling and SQLAlchemy integration.
* All chat history and logs are persisted in the database.

### 12-Factor Config Management

* All credentials, secrets, and port configurations are isolated in `.env` files.
* Nothing sensitive is committed to source code.

---

## Technology Stack

| Layer            | Technology                                    |
| ---------------- | --------------------------------------------- |
| LLM Runtime      | Gemma 3 (via OpenAI-compatible Docker Runner) |
| API Server       | FastAPI, Uvicorn                              |
| Agents           | LangGraph Supervisor and React Agents         |
| Database         | PostgreSQL 17, SQLModel                       |
| Email Tooling    | SMTP (smtplib), IMAP (imaplib)                |
| Containerization | Docker, Docker Compose                        |
| Auth Method      | Google App Passwords (requires 2FA)           |

---

## Architecture Overview

```
Supervisor Agent (LangGraph)
│
├── Research Agent 1 (React Agent)
│     └── Tools: Web Search, Summarization
│
├── Research Agent 2 (React Agent)
│     └── Tools: Composition, Email Drafting
│
└── Email Agent (Standalone)
      ├── send_email() → uses SMTP
      └── read_inbox() → uses IMAP
```

---

## Project Structure

```
Containarize_Agent/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── api/
│       │   ├── chat/        # chat endpoints, SQLModel models, logic
│       │   ├── ai/          # LangGraph agents, tools, LLM helpers
│       │   └── myemailer/   # SMTP/IMAP tools
│       └── main.py          # FastAPI entry-point
├── compose.yaml             # Docker Compose orchestration
├── .env.example_db          # Sample environment file for DB + API keys
└── README.md
```

---

## Quick Start

### 1. Prerequisites

* Docker version 24+
* Optional: Python 3.12 for manual development

### 2. Clone & Configure

```bash
git clone https://github.com/<your-username>/Containarize_Agent.git
cd Containarize_Agent

cp .env.example_db .env
cp backend/.env.example_db backend/.env
```

Edit `.env` and `backend/.env` to include:

```env
OPENAI_API_KEY=your_placeholder_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_google_app_password
```

### 3. Enable Google App Passwords

To use email features securely:

1. Go to: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Under "App passwords", generate a password for "Mail"
4. Paste that password into your `.env` as `EMAIL_PASSWORD`

### 4. Run with Docker Compose

```bash
docker compose up --build
```

Available services:

* API Docs: `http://localhost:8001/docs`
* PostgreSQL: `localhost:5432` (credentials in `.env`)
* OpenAI-Compatible Gemma 3 API: bound inside container

Hot-reloading is enabled for development inside `backend/src`.

---

## Running the Gemma 3 Model with Docker Model Runner

This project uses the [Docker Model Runner](https://replicate.com/docs/docker) to run the `ai/gemma3` model locally with an **OpenAI-compatible API**.

### 1. Pull the Model

```bash
docker model pull ai/gemma3
```

### 2. Run the Model

```bash
docker model run ai/gemma3
```

This launches a server at:

```
http://model-runner.docker.internal/engines/v1/chat/completions
```

This endpoint follows the **OpenAI Chat Completions format**, so you can plug it into tools like:

* **LangChain** via `OpenAI(base_url=..., api_key=...)`
* Your **FastAPI Supervisor Agent**, by routing calls to this URL.

### 3. Sample LangChain Configuration

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key="unused",  # any string, not validated
    openai_api_base="http://model-runner.docker.internal/engines/v1",
    model="ai/gemma3"
)
```

---

## Manual Run (Without Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
export $(cat .env | xargs)
cd backend/src
uvicorn main:app --reload
```

---

## API Reference

### `GET /`

Returns a basic health check.

### `POST /chat`

Send a query to the system. The Supervisor Agent will allocate it to one of the Research Agents, who may call tools or draft an email.

**Request:**

```json
{
  "message": "Find the benefits of morning exercise and email me the result."
}
```

**Response:**

```json
{
  "response": "Here is a summary of benefits of morning exercise...",
  "status": "email sent"
}
```

### `GET /chat/messages`

Lists all stored chat messages from the PostgreSQL database.

Interactive Swagger docs available at `http://localhost:8001/docs`.

---

## Production Deployment

### 1. Build Optimized Image

```bash
docker build -t containarize-agent:prod ./backend
```

