"""Raw SQL create chat_messages table

Revision ID: f456ad120936
Revises: f456ad120935
Create Date: 2025-09-12 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f456ad120936'
down_revision = 'f456ad120935'
branch_labels = None
depends_on = None


def upgrade():
    # Выполняем прямой SQL запрос для создания таблицы
    conn = op.get_bind()
    
    # Проверка наличия таблицы перед созданием
    result = conn.execute("SELECT to_regclass('public.chat_messages');").scalar()
    if result is None:  # Таблица не существует
        conn.execute("""
        CREATE TABLE chat_messages (
            id SERIAL PRIMARY KEY,
            conversation_id VARCHAR(64) NOT NULL,
            thread_id VARCHAR(64) NOT NULL,
            role VARCHAR(16) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX ix_chat_messages_conversation_id ON chat_messages (conversation_id);
        CREATE INDEX ix_chat_messages_thread_id ON chat_messages (thread_id);
        """)
        print("Таблица chat_messages успешно создана через SQL.")
    else:
        print("Таблица chat_messages уже существует, пропускаем создание.")


def downgrade():
    # Удаление таблицы, если она существует
    conn = op.get_bind()
    
    # Проверка наличия таблицы перед удалением
    result = conn.execute("SELECT to_regclass('public.chat_messages');").scalar()
    if result:  # Таблица существует
        conn.execute("""
        DROP TABLE IF EXISTS chat_messages CASCADE;
        """)
        print("Таблица chat_messages успешно удалена через SQL.")
    else:
        print("Таблица chat_messages не существует, пропускаем удаление.")
