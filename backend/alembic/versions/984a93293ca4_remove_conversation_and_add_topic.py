"""remove conversation and add topic

Revision ID: 984a93293ca4
Revises: abaa86708b54
Create Date: 2026-06-07 18:18:55.265846

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "984a93293ca4"
down_revision: Union[str, Sequence[str], None] = "abaa86708b54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE topic (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            title TEXT NOT NULL,
            summary TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ
        )
    """)

    op.execute("""
        INSERT INTO topic (id, title, summary, created_at)
        SELECT DISTINCT conversation_id, 'Topic migration', NULL, NOW()
        FROM messages
        WHERE conversation_id IS NOT NULL
        ON CONFLICT (id) DO NOTHING
    """)

    op.execute("""
        ALTER TABLE messages
        RENAME COLUMN conversation_id TO topic_id
    """)

    op.execute("""
        ALTER INDEX idx_messages_conversation_id
        RENAME TO idx_messages_topic_id
    """)

    op.execute("""
        ALTER TABLE messages
        DROP CONSTRAINT IF EXISTS messages_conversation_id_fkey
    """)

    op.execute("""
        ALTER TABLE messages
        ADD CONSTRAINT messages_topic_id_fkey
        FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE
    """)

    op.execute("DROP TABLE IF EXISTS conversations")


def downgrade() -> None:
    op.execute("""
        CREATE TABLE conversations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)

    op.execute("""
        ALTER TABLE messages
        DROP CONSTRAINT IF EXISTS messages_topic_id_fkey
    """)

    op.execute("""
        ALTER TABLE messages
        RENAME COLUMN topic_id TO conversation_id
    """)

    op.execute("""
        ALTER INDEX idx_messages_topic_id
        RENAME TO idx_messages_conversation_id
    """)

    op.execute("""
        ALTER TABLE messages
        ADD CONSTRAINT messages_conversation_id_fkey
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    """)

    op.execute("DROP TABLE IF EXISTS topic")
