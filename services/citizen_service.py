from db_configs.db_settings import execute_query, fetchall, fetchone


def vote_for_request():
    phone_number = input("Enter your phone number: ")
    citizen = fetchone("SELECT citizen_id, voted FROM citizens WHERE phone_number = %s", (phone_number,))

    if citizen and citizen[1]:
        print("You have already voted.")
        return

    requests = fetchall("SELECT request_id, request_text FROM requests WHERE status = 'accepted'")

    if not requests:
        print("No accepted requests to vote for.")
        return

    for req in requests:
        print(f"Request ID: {req[0]} - {req[1]}")

    vote_id = int(input("Enter the Request ID you want to vote for: "))

    if not citizen:
        execute_query("INSERT INTO citizens (phone_number, voted) VALUES (%s, TRUE) RETURNING citizen_id",
                      (phone_number,))
        citizen_id = fetchone("SELECT citizen_id FROM citizens WHERE phone_number = %s", (phone_number,))[0]
    else:
        citizen_id = citizen[0]
        execute_query("UPDATE citizens SET voted = TRUE WHERE citizen_id = %s", (citizen_id,))

    execute_query("INSERT INTO votes (request_id, citizen_id) VALUES (%s, %s)", (vote_id, citizen_id))
    print("Vote submitted successfully!")


def live_results():
    results = fetchall("""
        SELECT r.request_text, COUNT(v.vote_id) as vote_count
        FROM votes v
        JOIN requests r ON v.request_id = r.request_id
        WHERE r.status = 'accepted'
        GROUP BY r.request_text
        ORDER BY vote_count DESC
    """)

    print("Live Voting Results:")
    for res in results:
        print(f"{res[0]} - {res[1]} votes")


def citizen_menu():
    while True:
        print("\nCitizen Menu:")
        print("1. Vote for a Request")
        print("2. View Live Results")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            vote_for_request()
        elif choice == '2':
            live_results()
        elif choice == '3':
            break
