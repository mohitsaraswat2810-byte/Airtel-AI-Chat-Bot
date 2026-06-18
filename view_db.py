"""View database contents - Users, Conversations, and Messages."""

from db.connection import get_connection

conn = get_connection()
cursor = conn.cursor(dictionary=True)

print("\n" + "="*80)
print("USERS TABLE")
print("="*80)
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(f"ID: {row['id']}, Username: {row['username']}, Email: {row['email']}, Created: {row['created_at']}")

print("\n" + "="*80)
print("CONVERSATIONS TABLE")
print("="*80)
cursor.execute("SELECT * FROM conversations ORDER BY updated_at DESC")
for row in cursor.fetchall():
    print(f"ID: {row['id']}, User: {row['user_id']}, Title: {row['title']}, Updated: {row['updated_at']}")

print("\n" + "="*80)
print("MESSAGES TABLE (Recent 20)")
print("="*80)
cursor.execute("SELECT id, conversation_id, role, content, created_at FROM messages ORDER BY created_at DESC LIMIT 20")
for row in cursor.fetchall():
    content_preview = row['content'][:100].replace('\n', ' ')
    print(f"\nMsg ID {row['id']} | Conv {row['conversation_id']} | {row['role'].upper()}")
    print(f"  Content: {content_preview}...")
    print(f"  Time: {row['created_at']}")

cursor.close()
conn.close()
print("\n" + "="*80 + "\n")
