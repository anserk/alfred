LIST_ALL = """
    SELECT id, title, summary, created_at
    FROM topic t
    ORDER BY created_at ASC
"""

INSERT_NEW = """
INSERT INTO topic (id, title, summary, created_at)
VALUES
($1, $2, $3, now())
"""

UPDATE = """
UPDATE topic 
SET (updated_at, summary)
    = (now(), $2)
WHERE topic.id = $1
"""
