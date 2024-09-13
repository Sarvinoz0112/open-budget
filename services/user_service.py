import hashlib
from db_configs.db_settings import execute_query, fetchall, fetchone


def authenticate_user(username, password):
    """Authenticate a user."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = fetchone("""
    SELECT user_id FROM users WHERE username = %s AND password = %s AND role = 'user'
    """, (username, hashed_password))

    return user


def register_user():
    """Register a new user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        execute_query("""
        INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')
        """, (username, hashed_password))
        print("Registration successful.")
    except Exception as e:
        print(f"Error: {e}")


def login_user():
    """Log in a user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    user = authenticate_user(username, password)
    if user:
        print("Login successful.")
        return user[0]  # Returning the user ID
    else:
        print("Invalid credentials.")
        return None


def user_menu(user_id):
    """Display the user menu."""
    while True:
        print("\nUser Menu:")
        print("1. Create Project")
        print("2. Vote on Projects")
        print("3. View Results")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_project(user_id)
        elif choice == "2":
            vote_on_projects(user_id)
        elif choice == "3":
            view_results()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")


def create_project(user_id):
    """Create a new project."""
    category_id = input("Enter category ID: ").strip()
    project_name = input("Enter project name: ").strip()
    project_description = input("Enter project description: ").strip()
    budget = float(input("Enter project budget: ").strip())
    location = input("Enter project location: ").strip()

    try:
        execute_query("""
        INSERT INTO projects (user_id, category_id, project_name, project_description, budget, location, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'submitted')
        """, (user_id, category_id, project_name, project_description, budget, location))
        print("Project created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def vote_on_projects(user_id):
    """Vote on projects."""
    project_id = input("Enter project ID to vote for: ").strip()

    try:
        execute_query("""
        INSERT INTO votes (user_id, project_id) VALUES (%s, %s)
        """, (user_id, project_id))
        print("Vote recorded successfully.")
    except Exception as e:
        print(f"Error: {e}")


def view_results():
    """View results of voting."""
    results = fetchall("""
    SELECT projects.project_name, COUNT(votes.vote_id) AS vote_count
    FROM projects
    LEFT JOIN votes ON projects.project_id = votes.project_id
    GROUP BY projects.project_name
    """)
    for result in results:
        print(f"Project: {result[0]}, Votes: {result[1]}")
