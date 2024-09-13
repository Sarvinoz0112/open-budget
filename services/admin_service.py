from db_configs.db_settings import execute_query, fetchall


def accept_reject_requests():
    # Fetch pending requests
    requests = fetchall("SELECT request_id, request_text FROM requests WHERE status = 'pending'")

    if not requests:
        print("No pending requests.")
        return

    for req in requests:
        print(f"Request ID: {req[0]} - {req[1]}")
        action = input("Accept (A) or Reject (R)? ").lower()
        status = 'accepted' if action == 'a' else 'rejected'
        execute_query("UPDATE requests SET status = %s WHERE request_id = %s", (status, req[0]))
    print("Requests have been processed.")


def announce_winners():
    results = fetchall("""
        SELECT c.category_name, r.request_text, COUNT(v.vote_id) as vote_count
        FROM votes v
        JOIN requests r ON v.request_id = r.request_id
        JOIN categories c ON r.category_id = c.category_id
        WHERE r.status = 'accepted'
        GROUP BY c.category_name, r.request_text
        ORDER BY c.category_name, vote_count DESC
    """)

    print("Winners by Category:")
    current_category = None
    for res in results:
        if res[0] != current_category:
            current_category = res[0]
            print(f"\nCategory: {current_category}")
        print(f"{res[1]} - {res[2]} votes")


def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Accept/Reject Requests")
        print("2. Announce Winners")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            accept_reject_requests()
        elif choice == '2':
            announce_winners()
        elif choice == '3':
            break
