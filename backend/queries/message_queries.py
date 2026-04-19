LIST_ALL = """
    SELECT id, conversation_id, role, content, created_at
    FROM messages m
    ORDER BY created_at ASC
    limit $1
"""

INSERT_NEW = """
INSERT INTO messages (conversation_id, role, content)
VALUES
($1, $2, $3)
"""
