# Setup and Execution Guide

## Prerequisites

- Python 3.10+
- MySQL Server 8.0+
- Ollama installed for GPT-OSS inference

## Installation

1. Open a terminal in the project root.
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment template:

```bash
copy .env.example .env
```

4. Update `.env` with your MySQL credentials.

## Database Initialization

The app automatically initializes the database and tables on first launch using `db/schema.sql`.

## Running Ollama

Start the Ollama local API server:

```bash
ollama run gpt-oss:20b
```

## Launching the App

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`).

## Troubleshooting

- If MySQL cannot connect, verify `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
- If Ollama fails, ensure the model name in `.env` matches an installed Ollama model.
- If a required package is missing, reinstall with `pip install -r requirements.txt`.
