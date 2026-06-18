# Airtel-AI-Chat-Bot

An enterprise-grade AI chatbot application built with Streamlit, MySQL, and GPT-OSS integration. The project includes secure user authentication, persistent conversations, and a polished conversational UI for local deployment.

---

##  Features

- Streamlit-based web UI with chat and user management
- Local GPT-OSS inference through Ollama
- MySQL-backed persistence for users, conversations, and messages
- Secure registration and login with bcrypt password hashing
- Multi-conversation support with session state routing
- Modular architecture for auth, database, model, and pages

---

##  Prerequisites

- Python 3.10+
- MySQL Server 8.0+
- Ollama installed for GPT-OSS model hosting

---

##  Quick Start

1. Clone the repo and install dependencies:

```bash
cd Airtel
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update database and Ollama settings:

```bash
copy .env.example .env
# Edit .env with your MySQL credentials and preferences
```

3. Start Ollama with the GPT-OSS model:

```bash
ollama run gpt-oss:20b
```

4. Start MySQL and make sure it is available on `localhost:3306`.

5. Launch the app:

```bash
streamlit run app.py
```

The app creates the `chatbot_db` database and required tables on first launch.

---

##  Architecture

```text
Airtel/
├── app.py                  # Streamlit entry point for routing and UI
├── config.py               # Environment-driven configuration
├── requirements.txt        # Python dependency list
├── .env.example            # Environment variable template
├── auth/                   # Authentication and session management
│   ├── __init__.py
│   └── auth.py
├── db/                     # Database schema and connection utilities
│   ├── __init__.py
│   ├── schema.sql
│   └── connection.py
├── models/                 # GPT-OSS model client integration
│   ├── __init__.py
│   └── gpt_oss.py
└── pages/                  # Streamlit page modules for login/chat/register
    ├── login.py
    ├── register.py
    └── chat.py
```

---

##  Database Schema

### `users`

| Column        | Type         | Description                |
|---------------|--------------|----------------------------|
| id            | INT (PK)     | Auto-increment user ID     |
| username      | VARCHAR(50)  | Unique username            |
| email         | VARCHAR(100) | Unique email               |
| password_hash | VARCHAR(255) | bcrypt hash                |
| created_at    | TIMESTAMP    | Registration timestamp     |

### `conversations`

| Column     | Type          | Description                    |
|------------|---------------|--------------------------------|
| id         | INT (PK)      | Auto-increment conversation ID |
| user_id    | INT (FK)      | Owner → users.id               |
| title      | VARCHAR(255)  | Conversation title             |
| created_at | TIMESTAMP     | Creation time                  |
| updated_at | TIMESTAMP     | Last activity                  |

### `messages`

| Column          | Type          | Description                    |
|-----------------|---------------|--------------------------------|
| id              | INT (PK)      | Auto-increment message ID      |
| conversation_id | INT (FK)      | Parent → conversations.id      |
| role            | ENUM          | user / assistant / system      |
| content         | TEXT          | Message body                   |
| created_at      | TIMESTAMP     | Send time                      |

---

##  Configuration

All settings are loaded from environment variables (see `.env.example`):

| Variable            | Default                         | Description               |
|---------------------|---------------------------------|---------------------------|
| `DB_HOST`           | `localhost`                     | MySQL host                |
| `DB_PORT`           | `3306`                          | MySQL port                |
| `DB_USER`           | `root`                          | MySQL username            |
| `DB_PASSWORD`       | *(empty)*                       | MySQL password            |
| `DB_NAME`           | `chatbot_db`                    | Database name             |
| `OLLAMA_BASE_URL`   | `http://localhost:11434/v1`     | Ollama API endpoint       |
| `MODEL_NAME`        | `gpt-oss:20b`                   | Model to use              |
| `MODEL_TEMPERATURE` | `0.7`                           | Generation temperature    |
| `MODEL_MAX_TOKENS`  | `2048`                          | Max response length       |

---

##  License

This project is provided for educational and development purposes.
