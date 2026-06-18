"""
MySQL Database Connection and CRUD Operations.

Provides a connection pool, context-managed cursor, database initialization,
and all CRUD operations for users, conversations, and messages.
"""

import os
import mysql.connector
from mysql.connector import pooling, Error
from config import DB_CONFIG

# ─── Connection Pool (lazy-initialized) ─────────────────────────────
_pool = None


def _get_pool():
    """Get or create the MySQL connection pool."""
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="chatbot_pool",
            pool_size=5,
            pool_reset_session=True,
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset="utf8mb4",
            collation="utf8mb4_general_ci",
        )
    return _pool


def get_connection():
    """Get a connection from the pool."""
    return _get_pool().get_connection()


def init_db():
    """
    Initialize the database by executing the schema SQL.
    Creates the database and tables if they don't already exist.
    """
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()

    # Execute each statement individually
    for statement in schema.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════
# User Operations
# ═══════════════════════════════════════════════════════════════════════

def create_user(username, email, password_hash):
    """
    Create a new user account.

    Args:
        username: Unique username.
        email: User's email address.
        password_hash: bcrypt-hashed password string.

    Returns:
        int: The new user's ID.

    Raises:
        mysql.connector.Error: On duplicate username/email or DB failure.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash),
        )
        conn.commit()
        return cursor.lastrowid
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_user_by_username(username):
    """
    Retrieve a user by username.

    Returns:
        dict | None: User record as a dictionary, or None if not found.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_user_by_email(email):
    """
    Retrieve a user by email address.

    Returns:
        dict | None: User record as a dictionary, or None if not found.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


# ═══════════════════════════════════════════════════════════════════════
# Conversation Operations
# ═══════════════════════════════════════════════════════════════════════

def create_conversation(user_id, title="New Conversation"):
    """
    Create a new conversation for a user.

    Args:
        user_id: The owning user's ID.
        title: Initial conversation title.

    Returns:
        int: The new conversation's ID.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_id, title) VALUES (%s, %s)",
            (user_id, title),
        )
        conn.commit()
        return cursor.lastrowid
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_conversations_by_user(user_id):
    """
    Get all conversations for a user, most recent first.

    Returns:
        list[dict]: List of conversation records.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM conversations WHERE user_id = %s ORDER BY updated_at DESC",
            (user_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def update_conversation_title(conversation_id, title):
    """Update the title of an existing conversation."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE conversations SET title = %s WHERE id = %s",
            (title, conversation_id),
        )
        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def delete_conversation(conversation_id):
    """Delete a conversation and all its messages (cascaded)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))
        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


# ═══════════════════════════════════════════════════════════════════════
# Message Operations
# ═══════════════════════════════════════════════════════════════════════

def add_message(conversation_id, role, content):
    """
    Add a message to a conversation.

    Args:
        conversation_id: The conversation to add to.
        role: Message role — 'user', 'assistant', or 'system'.
        content: The message text.

    Returns:
        int: The new message's ID.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s)",
            (conversation_id, role, content),
        )
        conn.commit()
        return cursor.lastrowid
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_messages_by_conversation(conversation_id):
    """
    Get all messages in a conversation, ordered chronologically.

    Returns:
        list[dict]: List of message records.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM messages WHERE conversation_id = %s ORDER BY created_at ASC",
            (conversation_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
