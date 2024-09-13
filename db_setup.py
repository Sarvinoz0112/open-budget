from db_configs.db_settings import execute_query

def create_tables():
    """Create tables in the database."""
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL
    );
    """

    projects_table = """
    CREATE TABLE IF NOT EXISTS projects (
        project_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        category_id INTEGER,
        project_name VARCHAR(255) NOT NULL,
        project_description TEXT,
        budget DECIMAL(10, 2),
        location VARCHAR(255),
        status VARCHAR(50) DEFAULT 'submitted'
    );
    """

    votes_table = """
    CREATE TABLE IF NOT EXISTS votes (
        vote_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        project_id INTEGER REFERENCES projects(project_id)
    );
    """

    execute_query(users_table)
    execute_query(projects_table)
    execute_query(votes_table)

if __name__ == "__main__":
    create_tables()
