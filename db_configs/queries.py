from db_configs.db_settings import fetchone, execute_query, fetchall
from datetime import datetime

def create_user_table():
    return """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'user'
    );
    """

def create_project_table():
    return """
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        description TEXT,
        budget DECIMAL NOT NULL,
        location VARCHAR(100) NOT NULL,
        approved BOOLEAN DEFAULT FALSE
    );
    """

def create_season_table():
    return """
    CREATE TABLE IF NOT EXISTS season (
        id SERIAL PRIMARY KEY,
        name varchar(255) NOT NULL,
        is_open BOOLEAN NOT NULL,
        open_time TIMESTAMP,
        close_time TIMESTAMP
    );
    """


def view_all_seasons_with_status():
    query = """
        SELECT 
            name, 
            open_time, 
            close_time, 
            CASE 
                WHEN NOW() BETWEEN open_time AND close_time THEN 'Open' 
                ELSE 'Closed' 
            END AS status
        FROM season
        ORDER BY open_time DESC;
    """
    return fetchall(query)


def insert_user():
    return """
    INSERT INTO users (username, password, role) VALUES (%s, %s, %s);
    """

def select_user_by_username():
    return """
    SELECT * FROM users WHERE username = %s;
    """

def insert_project():
    return """
    INSERT INTO projects (name, category, description, budget, location, approved) VALUES (%s, %s, %s, %s, %s, %s);
    """

def get_season_status():
    query = "SELECT is_open, open_time, close_time FROM season ORDER BY id DESC LIMIT 1;"
    result = fetchone(query)
    return result


def open_season(season_name, open_time, close_time=None):
    query = """
    INSERT INTO season (name, is_open, open_time, close_time)
    VALUES (%s, TRUE, %s, %s);
    """
    execute_query(query, (season_name, open_time, close_time))

def close_season(season_name, close_time):
    query = """
    UPDATE season
    SET is_open = FALSE, close_time = %s
    WHERE name = %s AND is_open = TRUE;
    """
    execute_query(query, (close_time, season_name))


def is_season_active():
    status = get_season_status()
    if status:
        is_open, open_time, close_time = status
        if is_open:
            return True
        if close_time and datetime.now() >= close_time:
            # Close the season if the current time is past the close time
            close_season(close_time)
            return False
    return False
def update_project_approval():
    return """
    UPDATE projects SET approved = TRUE WHERE id = %s;
    """

def update_project_rejection():
    return """
    UPDATE projects SET approved = FALSE WHERE id = %s;
    """

def select_all_projects():
    return """
    SELECT * FROM projects;
    """

def select_all_approved_projects():
    return """
    SELECT * FROM projects WHERE approved = TRUE;
    """

def select_all_rejected_projects():
    return """
    SELECT * FROM projects WHERE approved = FALSE;
    """
