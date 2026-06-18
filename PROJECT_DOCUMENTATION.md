# Project Documentation

## Overview

The Airtel project is an AI chatbot application built with Streamlit, MySQL, and GPT-OSS via Ollama. It supports user registration, login, chat conversations, and message history persistence.

## Architecture

- `app.py`: Streamlit entry point, routing, and UI orchestration.
- `config.py`: Loads environment variables and centralizes app configuration.
- `auth/auth.py`: User registration, login, and session handling.
- `db/connection.py`: MySQL connection pool and CRUD operations.
- `db/schema.sql`: Database schema definition for users, conversations, and messages.
- `models/gpt_oss.py`: GPT-OSS client wrapper using the Ollama-compatible API.
- `pages/login.py`: Login page UI.
- `pages/register.py`: Registration page UI.
- `pages/chat.py`: Main chat interface.

## Key Features

- Authentication with bcrypt password hashing
- Persistent user conversations in MySQL
- Multiple conversation support
- GPT-OSS integration via local Ollama API
- Streamlit-based UI with session management

## Database Schema

The database schema is defined in `db/schema.sql`.

### Tables

- `users`
- `conversations`
- `messages`

## Dependencies

Dependencies are listed in `requirements.txt`.

## Environment Variables

The `.env.example` file contains template environment variables.
