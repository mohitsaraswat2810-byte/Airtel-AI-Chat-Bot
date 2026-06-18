"""
Centralized Configuration for the AI Chatbot Application.

Loads settings from environment variables with sensible defaults.
Uses python-dotenv to support .env files for local development.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── Database Configuration ──────────────────────────────────────────
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "chatbot_db"),
}

# ─── GPT-OSS / Ollama Configuration ─────────────────────────────────
MODEL_CONFIG = {
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    "model_name": os.getenv("MODEL_NAME", "gpt-oss:20b"),
    "temperature": float(os.getenv("MODEL_TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("MODEL_MAX_TOKENS", "2048")),
    "api_key": os.getenv("OLLAMA_API_KEY", "ollama"),  # Ollama doesn't require a real key
}

# ─── App Configuration ───────────────────────────────────────────────
APP_CONFIG = {
    "app_name": os.getenv("APP_NAME", "AI Chatbot"),
    "page_icon": "🤖",
}
