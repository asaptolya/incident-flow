# 🚨 IncidentFlow

IncidentFlow is a lightweight **incident monitoring and alert management system** built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, and Telegram.

It accepts events from external services through a REST API, automatically creates incidents, stores them in PostgreSQL, and sends real-time notifications to Telegram.

The project demonstrates an asynchronous Python backend with database persistence, migrations, API documentation, and Telegram Bot integration.

---

## ✨ Features

- REST API built with FastAPI
- Asynchronous PostgreSQL integration
- SQLAlchemy ORM
- Alembic database migrations
- Incident lifecycle management
- Automatic incident creation from incoming events
- Automatic severity mapping
- Telegram notifications
- Interactive Telegram inline actions
- Incident acknowledgement
- Incident resolution
- Swagger / OpenAPI documentation
- Dockerized PostgreSQL
- Environment-based configuration
- Modular backend architecture

---

## 🛠 Tech Stack

- **Python 3.11+**
- **FastAPI**
- **aiogram 3**
- **PostgreSQL**
- **SQLAlchemy**
- **asyncpg**
- **Alembic**
- **Pydantic**
- **Docker**
- **Docker Compose**
- **Uvicorn**

---

## 🏗 Architecture

```text
External Service
       |
       v
+------------------+
|    FastAPI API   |
+------------------+
       |
       v
+------------------+
|  Incident Logic  |
+------------------+
       |
       +-------------------+
       |                   |
       v                   v
+--------------+     +----------------+
| PostgreSQL   |     | Telegram Bot   |
| Database     |     | Notifications  |
+--------------+     +----------------+
```

Incoming events are processed by the API and converted into incidents.

Each incident is persisted in PostgreSQL and can trigger a Telegram notification with interactive controls for acknowledging or resolving the incident.

---

## 📁 Project Structure

```text
incidentflow/
|
├── alembic/
│   └── versions/
│
├── app/
│   ├── api/
│   │   ├── events.py
│   │   ├── health.py
│   │   └── incidents.py
│   │
│   ├── bot/
│   │   ├── bot.py
│   │   ├── handlers.py
│   │   └── keyboards.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── event.py
│   │   └── incident.py
│   │
│   ├── schemas/
│   │   ├── event.py
│   │   └── incident.py
│   │
│   ├── services/
│   │   ├── incident_service.py
│   │   └── notification_service.py
│   │
│   └── main.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔄 Incident Lifecycle

Incidents can have the following statuses:

```text
open
  |
  v
acknowledged
  |
  v
resolved
```

Each incident also has a severity level:

```text
low
medium
high
critical
```

Incoming event levels are automatically mapped to incident severity:

```text
info      -> low
warning   -> medium
error     -> high
critical  -> critical
```

---

## 🌐 API

FastAPI automatically generates interactive OpenAPI documentation.

After starting the application, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "IncidentFlow"
}
```

---

## 📡 Create an Event

```http
POST /api/events
```

Example request:

```json
{
  "service": "payment-api",
  "level": "critical",
  "message": "Database connection failed"
}
```

IncidentFlow automatically creates an incident associated with the event.

Example response:

```json
{
  "id": 1,
  "service": "payment-api",
  "level": "critical",
  "message": "Database connection failed",
  "incident_id": 1,
  "created_at": "2026-08-30T12:00:00"
}
```

---

## 🚨 Incidents

### Get all incidents

```http
GET /api/incidents
```

### Get incident by ID

```http
GET /api/incidents/{incident_id}
```

### Update incident

```http
PATCH /api/incidents/{incident_id}
```

Example request:

```json
{
  "status": "resolved"
}
```

---

## 🤖 Telegram Notifications

When a new incident is created, IncidentFlow can automatically send a notification to a configured Telegram chat.

Example notification:

```text
🚨 CRITICAL INCIDENT

Service: payment-api
Incident: #1

Database connection failed

Status: open
```

The notification includes interactive controls:

```text
[ 👤 Acknowledge ] [ ✅ Resolve ]
```

These actions update the incident directly in PostgreSQL.

For example:

```text
open -> acknowledged -> resolved
```

This allows incidents to be managed directly from Telegram without manually accessing the API.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/asaptolya/incidentflow.git
cd incidentflow
```

### Create a virtual environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`.

```env
APP_NAME=IncidentFlow
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incidentflow
DATABASE_URL_SYNC=postgresql+psycopg://postgres:postgres@localhost:5432/incidentflow

TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

Never commit your real `.env` file, Telegram bot token, or other credentials.

---

## 🐳 Start PostgreSQL

The project includes a Docker Compose configuration for PostgreSQL.

Make sure Docker is running and execute:

```bash
docker compose up -d
```

Check that the container is running:

```bash
docker ps
```

You should see the PostgreSQL container:

```text
incidentflow-postgres
```

To stop the containers:

```bash
docker compose down
```

---

## 🗄 Database Migrations

Apply all existing migrations:

```bash
alembic upgrade head
```

When database models are changed, create a new migration:

```bash
alembic revision --autogenerate -m "migration description"
```

Apply it:

```bash
alembic upgrade head
```

---

## ▶️ Run the Application

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

If port `8000` is already in use, another port can be specified:

```bash
uvicorn app.main:app --reload --port 8001
```

---

## 💡 Example Workflow

A monitored application sends an event:

```json
{
  "service": "auth-service",
  "level": "critical",
  "message": "Authentication database is unreachable"
}
```

IncidentFlow then:

1. Receives the event through the REST API
2. Validates the incoming data
3. Stores the event
4. Creates a new incident
5. Maps the event level to an incident severity
6. Persists the incident in PostgreSQL
7. Sends a real-time Telegram notification
8. Allows the incident to be acknowledged or resolved directly from Telegram

The complete flow looks like this:

```text
Application
    |
    | POST /api/events
    v
FastAPI
    |
    v
Event Processing
    |
    v
Incident Creation
    |
    +-----------> PostgreSQL
    |
    v
Telegram Alert
    |
    v
Acknowledge / Resolve
    |
    v
PostgreSQL Update
```

---

## 🔒 Security

Sensitive configuration is stored using environment variables.

The following files and directories are excluded from Git:

```text
.env
.venv/
__pycache__/
.idea/
```

The repository contains `.env.example` instead of real credentials.

---

## 🗺 Roadmap

Possible future improvements:

- API key authentication
- Rate limiting
- Incident filtering
- Pagination
- Event history endpoints
- Multiple Telegram chats
- Webhook support
- Redis
- Background workers
- User authentication
- Incident assignment
- Metrics and analytics
- Automated tests
- CI/CD pipeline
- Additional notification channels

---

## 🎯 Project Purpose

IncidentFlow was created as a backend portfolio project demonstrating practical experience with:

- asynchronous Python development
- REST API design
- FastAPI
- Telegram Bot API integration
- relational database design
- PostgreSQL
- SQLAlchemy ORM
- database migrations
- Docker
- asynchronous application architecture
- modular backend development

---

## 📄 License

This project is available for educational and portfolio purposes.