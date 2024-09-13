from db_configs.db_settings import execute_query

def create_tables():
    # SQL for creating the categories table
    create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(50) NOT NULL
    );
    """
    # SQL for creating the requests table
    create_requests_table = """
    CREATE TABLE IF NOT EXISTS requests (
        request_id SERIAL PRIMARY KEY,
        request_text TEXT NOT NULL,
        status VARCHAR(10) NOT NULL,  -- 'pending', 'accepted', or 'rejected'
        category_id INT NOT NULL REFERENCES categories(category_id)
    );
    """
    # SQL for creating the citizens table
    create_citizens_table = """
    CREATE TABLE IF NOT EXISTS citizens (
        citizen_id SERIAL PRIMARY KEY,
        phone_number VARCHAR(15) UNIQUE NOT NULL,
        voted BOOLEAN DEFAULT FALSE
    );
    """
    # SQL for creating the votes table
    create_votes_table = """
    CREATE TABLE IF NOT EXISTS votes (
        vote_id SERIAL PRIMARY KEY,
        request_id INT NOT NULL REFERENCES requests(request_id),
        citizen_id INT NOT NULL REFERENCES citizens(citizen_id)
    );
    """

    # Execute the queries
    execute_query(create_categories_table)
    execute_query(create_requests_table)
    execute_query(create_citizens_table)
    execute_query(create_votes_table)

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully (if they didn't exist).")
