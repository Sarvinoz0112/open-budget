from service.auth import register_user, login_user, check_admin
from service.project import create_project, approve_project, reject_project, view_all_projects, \
    view_all_approved_projects, view_all_rejected_projects
from db_configs.db_settings import execute_query
from db_configs.queries import create_user_table, create_project_table, open_season, close_season, get_season_status, \
    create_season_table, view_all_seasons_with_status
from tabulate import tabulate
from datetime import datetime

def create_tables():
    execute_query(create_user_table())
    execute_query(create_project_table())
    execute_query(create_season_table())


def display_results(results, headers):
    if results:
        table = tabulate(results, headers=headers, tablefmt="grid")
        print(table)
    else:
        print("No results were found.")


def user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. Create Project")
        print("2. View My All Created Projects")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            print("Categories:")
            print("1. Local Infrastructure Improvement")
            print("2. Social Services")
            print("3. Culture and Sports")
            print("4. Environmental Protection")
            category = input("Select category (1-4): ")
            category_map = {
                '1': 'Local Infrastructure Improvement',
                '2': 'Social Services',
                '3': 'Culture and Sports',
                '4': 'Environmental Protection'
            }
            category = category_map.get(category, 'Unknown')
            name = input("Enter project name: ")
            description = input("Enter project description: ")
            budget = float(input("Enter project budget: "))
            print("Regions:")
            print("1. Tashkent Region")
            print("2. Andijan Region")
            print("3. Bukhara Region")
            print("4. Fergana  Region")
            print("5. Jizzakh Region")
            print("6. Khorezm Region")
            print("7. Namangan Region")
            print("8. Navoi Region")
            print("9. Kashkadarya Region")
            print("10. Samarkand Region")
            print("11. Syrdarya Region")
            print("12. Surkhandarya Region")
            print("13. Republic of Karakalpakstan")

            region = input("Select region: ")

            result = create_project(category, name, description, budget, region)
            print(result)

        elif choice == '2':
            projects = view_all_projects()
            headers = ["ID", "Name", "Category", "Description", "Budget", "Location", "Approved"]
            display_results(projects, headers)

        elif choice == '3':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Open/Close Season")
        print("2. Manage Submissions")
        print("   a. View All Projects")
        print("   b. Approve Project")
        print("   c. Reject Project")
        print("3. View All Approved Projects")
        print("4. View All Rejected Projects")
        print("5. View All Seasons with Status")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            action = input("Do you want to (o)pen or (c)lose a season? (o/c): ").strip().lower()
            if action == 'o':
                season_name = input("Enter the name of the new season: ")
                open_time_input = input("Enter opening time (YYYY-MM-DD HH:MM:SS): ")
                close_time_input = input("Enter closing time (YYYY-MM-DD HH:MM:SS): ")
                try:
                    open_time = datetime.strptime(open_time_input, '%Y-%m-%d %H:%M:%S')
                    close_time = datetime.strptime(close_time_input, '%Y-%m-%d %H:%M:%S')
                    open_season(season_name, open_time, close_time)
                    print(f"New season '{season_name}' has been opened.")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")

            elif action == 'c':
                season_name = input("Enter the name of the season to close: ")
                close_time_input = input("Enter closing time (YYYY-MM-DD HH:MM:SS): ")
                try:
                    close_time = datetime.strptime(close_time_input, '%Y-%m-%d %H:%M:%S')
                    close_season(season_name, close_time)
                    print(f"Season '{season_name}' has been closed.")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")

        elif choice == '2':
            sub_choice = input("Select Manage Submissions option (a-c): ")
            if sub_choice == 'a':
                projects = view_all_projects()
                headers = ["ID", "Name", "Category", "Description", "Budget", "Location", "Approved"]
                display_results(projects, headers)

            elif sub_choice == 'b':
                project_id = int(input("Enter project ID to approve: "))
                result = approve_project(project_id)
                print(result)

            elif sub_choice == 'c':
                project_id = int(input("Enter project ID to reject: "))
                result = reject_project(project_id)
                print(result)

            else:
                print("Invalid choice. Please try again.")

        elif choice == '3':
            projects = view_all_approved_projects()
            headers = ["ID", "Name", "Category", "Description", "Budget", "Location", "Approved"]
            display_results(projects, headers)

        elif choice == '4':
            projects = view_all_rejected_projects()
            headers = ["ID", "Name", "Category", "Description", "Budget", "Location", "Approved"]
            display_results(projects, headers)

        elif choice == '5':
            seasons = view_all_seasons_with_status()
            headers = ["Season Name", "Open Time", "Close Time", "Status"]
            display_results(seasons, headers)

        elif choice == '6':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = register_user(username, password)
            print(result)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = login_user(username, password)
            if 'error' in result:
                print(result['error'])
            else:
                if check_admin(username, password):
                    admin_menu()
                else:
                    user_menu()

        elif choice == '3':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    create_tables()
    main_menu()
