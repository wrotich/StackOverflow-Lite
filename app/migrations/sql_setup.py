"""
    This file contains commands for creating/dropping tables in the db.
"""
drop_tables_commands = (
    """
    DROP TABLE IF EXISTS users CASCADE
    """,
    """
    DROP TABLE IF EXISTS questions CASCADE
    """,
    """
    DROP TABLE IF EXISTS answers CASCADE
    """,
)
drop_answers = (
    """
    DROP TABLE IF EXISTS answers CASCADE
    """,
)


create_tables_commands = (
    """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(500) NOT NULL,
        created_at timestamp with time zone DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS questions(
        question_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        body text NOT NULL,
        created_at timestamp with time zone DEFAULT now(),
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS answers(
        answer_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        answer_body TEXT NOT NULL,
        accepted bool DEFAULT false,
        username TEXT NOT NULL,
        created_at timestamp with time zone DEFAULT now(),
        FOREIGN KEY (question_id)
            REFERENCES  questions (question_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON UPDATE CASCADE ON DELETE CASCADE            
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tokens(
        user_id SERIAL PRIMARY KEY,
        token VARCHAR NOT NULL
    )""",
)

migrations = create_tables_commands
