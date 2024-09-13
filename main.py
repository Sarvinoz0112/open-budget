import hashlib
from services.admin_service import admin_menu
from services.user_service import user_menu, register_user, login_user
from db_setup import create_tables

def main_menu():
    """Display the main menu."""
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
            if user_id:
                user_menu(user_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    create_tables()
    while True:
        print("\nWelcome to Budget.uz Platform")
        print("1. Admin Login")
        print("2. User Menu")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            admin_menu()
        elif choice == "2":
            main_menu()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")
