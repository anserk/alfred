LIST_ALL = """
    SELECT id, topic_id, role, content, created_at
    FROM messages m
    ORDER BY created_at ASC
    limit $1
"""

INSERT_NEW = """
INSERT INTO messages (topic_id, role, content)
VALUES
($1, $2, $3)
"""
