from db_configs.db_settings import execute_query, fetchall, fetchone
import hashlib


def authenticate_admin():
    """Authenticate admin user."""
    username = "admin"
    password = "admin"

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    admin = fetchone("""
    SELECT id FROM users WHERE username = %s AND password = %s AND role = 'admin'
    """, (username, hashed_password))
    if admin:
        return {'who': 'admin'}
    return None

def admin_menu():
    """Display the admin menu."""
    if not authenticate_admin():
        print("Admin authentication failed.")
        return

    while True:
        print("\nAdmin Menu:")
        print("1. Open/Close Season")
        print("2. Set Categories")
        print("3. Update Rules")
        print("4. Manage Submissions")
        print("5. Manage Voting")
        print("6. View Statistics")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            open_close_season()
        elif choice == "2":
            set_categories()
        elif choice == "3":
            update_rules()
        elif choice == "4":
            manage_submissions()
        elif choice == "5":
            manage_voting()
        elif choice == "6":
            view_statistics()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")


def open_close_season():
    """Open or close the season."""
    print("Season opening/closing functionality")
    action = input("Enter 'open' to open the season or 'close' to close it: ").strip().lower()
    if action == 'open':
        print("Season is now open.")
    elif action == 'close':
        print("Season is now closed.")
    else:
        print("Invalid action. Please enter 'open' or 'close'.")


def set_categories():
    """Set categories for the season."""
    print("Setting categories functionality")
    category_name = input("Enter category name to add: ").strip()
    print(f"Category '{category_name}' added.")


def update_rules():
    """Update the rules for the season."""
    print("Updating rules functionality")
    new_rules = input("Enter the new rules: ").strip()
    print(f"Rules updated to: {new_rules}")


def manage_submissions():
    """Manage project submissions."""
    print("Managing submissions functionality")
    action = input("Enter 'approve' to approve submissions or 'reject' to reject: ").strip().lower()
    if action == 'approve':
        print("Submissions approved.")
    elif action == 'reject':
        print("Submissions rejected.")
    else:
        print("Invalid action. Please enter 'approve' or 'reject'.")


def manage_voting():
    """Manage the voting process."""
    print("Managing voting functionality")
    action = input("Enter 'start' to start voting or 'end' to end voting: ").strip().lower()
    if action == 'start':
        print("Voting started.")
    elif action == 'end':
        print("Voting ended.")
    else:
        print("Invalid action. Please enter 'start' or 'end'.")


def view_statistics():
    """View statistics for the season."""
    results = fetchall("""
    SELECT projects.project_name, COUNT(votes.vote_id) AS vote_count
    FROM projects
    LEFT JOIN votes ON projects.project_id = votes.project_id
    GROUP BY projects.project_name
    """)
    for result in results:
        print(f"Project: {result[0]}, Votes: {result[1]}")
