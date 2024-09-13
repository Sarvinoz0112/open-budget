from services.admin_service import admin_menu
from services.citizen_service import citizen_menu
from db_setup import create_tables  # Import the setup script

if __name__ == "__main__":
    # Create the necessary tables
    create_tables()

    while True:
        print("\nMain Menu:")
        print("1. Admin")
        print("2. Citizen")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            admin_menu()
        elif choice == '2':
            citizen_menu()
        elif choice == '3':
            break
