from db_configs.db_settings import Database
from services.admin_service import authenticate_admin
import hashlib

db = Database()


def register_user():
    """Register a new user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    db.execute("""
    INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')
    """, (username, hashed_password))
    print("User registered successfully.")


def login_user():
    """Login a user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if username == 'admin' and password == 'admin':
        return authenticate_admin()
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = db.fetchone("""
        SELECT id FROM users WHERE username = %s AND password = %s AND role = 'user'
        """, (username, hashed_password))

        return {'who': 'user', 'user_id': user[0]} if user else None


def user_menu():
    """Display the user menu."""
    while True:
        print("\nUser Menu:")
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
            if user_id:
                user_dashboard(user_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")


def user_dashboard(user_id):
    """Display the user dashboard after login."""
    while True:
        print("\nUser Dashboard:")
        print("1. Create Project")
        print("2. Vote on Projects")
        print("3. View Results")
        print("0. Logout")
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
    project_name = input("Enter project name: ").strip()
    project_description = input("Enter project description: ").strip()
    project_budget = input("Enter project budget: ").strip()
    project_location = input("Enter project location: ").strip()

    db.execute("""
    INSERT INTO projects (id, project_name, project_description, budget, location) VALUES (%s, %s, %s, %s, %s)
    """, (user_id, project_name, project_description, project_budget, project_location))
    print("Project created successfully.")


def vote_on_projects(id):
    """Vote on projects."""
    project_id = input("Enter project ID to vote for: ").strip()
    db.execute("""
    INSERT INTO votes (id, project_id) VALUES (%s, %s)
    """, (id, project_id))
    print("Vote submitted successfully.")


def view_results():
    """View voting results."""
    results = db.fetchall("""
    SELECT projects.project_name, COUNT(votes.vote_id) AS vote_count
    FROM projects
    LEFT JOIN votes ON projects.project_id = votes.project_id
    GROUP BY projects.project_name
    """)
    for result in results:
        print(f"Project: {result[0]}, Votes: {result[1]}")
