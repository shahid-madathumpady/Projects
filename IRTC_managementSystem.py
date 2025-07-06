import sqlite3

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Connect to SQLite
conn = sqlite3.connect("booking_system.db")
cursor = conn.cursor()

# Create tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS train_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT, source TEXT, destination TEXT, departure_time TEXT, arrival_time TEXT
);
CREATE TABLE IF NOT EXISTS flight_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_no TEXT, from_city TEXT, to_city TEXT, departure_time TEXT, arrival_time TEXT
);
CREATE TABLE IF NOT EXISTS hotel_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_name TEXT, city TEXT, checkin TEXT, checkout TEXT
);
CREATE TABLE IF NOT EXISTS railway_bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, train_id INTEGER, travel_date TEXT,
    FOREIGN KEY(train_id) REFERENCES train_schedule(id)
);
CREATE TABLE IF NOT EXISTS airline_bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, flight_id INTEGER, travel_date TEXT,
    FOREIGN KEY(flight_id) REFERENCES flight_schedule(id)
);
CREATE TABLE IF NOT EXISTS hotel_bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, hotel_id INTEGER,
    FOREIGN KEY(hotel_id) REFERENCES hotel_schedule(id)
);
''')

# Admin login
def admin_login():
    print("\n🔐 Admin Login Required")
    username = input("Username: ")
    password = input("Password: ")
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# Seeding sample schedules
def seed_schedules():
    cursor.executemany("INSERT INTO train_schedule (train_name, source, destination, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)", [
        ("Express 101", "Delhi", "Mumbai", "06:00", "16:00"),
        ("Shatabdi", "Chennai", "Bangalore", "07:30", "12:30")
    ])
    cursor.executemany("INSERT INTO flight_schedule (flight_no, from_city, to_city, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)", [
        ("AI202", "Kochi", "Delhi", "09:00", "13:00"),
        ("6E456", "Mumbai", "Hyderabad", "15:00", "17:00")
    ])
    cursor.executemany("INSERT INTO hotel_schedule (hotel_name, city, checkin, checkout) VALUES (?, ?, ?, ?)", [
        ("Taj Hotel", "Delhi", "2025-07-10", "2025-07-12"),
        ("Hilton", "Bangalore", "2025-07-15", "2025-07-18")
    ])
    conn.commit()
    print("✅ Schedules seeded.")

# View schedules
def view_schedule(table):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Booking functions
def book_train():
    view_schedule("train_schedule")
    name = input("Name: ")
    train_id = int(input("Train ID: "))
    date = input("Travel Date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO railway_bookings (name, train_id, travel_date) VALUES (?, ?, ?)", (name, train_id, date))
    conn.commit()
    print("✅ Train booked!")

def book_flight():
    view_schedule("flight_schedule")
    name = input("Name: ")
    flight_id = int(input("Flight ID: "))
    date = input("Travel Date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO airline_bookings (name, flight_id, travel_date) VALUES (?, ?, ?)", (name, flight_id, date))
    conn.commit()
    print("✅ Flight booked!")

def book_hotel():
    view_schedule("hotel_schedule")
    name = input("Name: ")
    hotel_id = int(input("Hotel ID: "))
    cursor.execute("INSERT INTO hotel_bookings (name, hotel_id) VALUES (?, ?)", (name, hotel_id))
    conn.commit()
    print("✅ Hotel booked!")

# Search
def search_booking(table, join_table, keyword_column, display_columns):
    keyword = input("Search by Name or ID: ")
    if keyword.isdigit():
        query = f"SELECT * FROM {table} WHERE {keyword_column} = ?"
        cursor.execute(query, (int(keyword),))
    else:
        query = f"SELECT * FROM {table} WHERE name LIKE ?"
        cursor.execute(query, ('%' + keyword + '%',))
    rows = cursor.fetchall()
    for row in rows:
        print(dict(zip(display_columns, row)))

# Admin-protected actions
def delete_booking(table):
    if not admin_login():
        print("❌ Access denied.")
        return
    bid = input("Enter Booking ID to delete: ")
    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (bid,))
    conn.commit()
    print("✅ Deleted.")

def update_train_date():
    if not admin_login():
        print("❌ Access denied.")
        return
    bid = input("Booking ID: ")
    new_date = input("New Date (YYYY-MM-DD): ")
    cursor.execute("UPDATE railway_bookings SET travel_date = ? WHERE id = ?", (new_date, bid))
    conn.commit()
    print("✅ Updated.")

# Menu
def main_menu():
    while True:
        print("\n📍 Booking System")
        print("1. Seed Sample Schedules")
        print("2. View Train Schedule")
        print("3. View Flight Schedule")
        print("4. View Hotel Schedule")
        print("5. Book Train")
        print("6. Book Flight")
        print("7. Book Hotel")
        print("8. Search Train Booking")
        print("9. Search Flight Booking")
        print("10. Search Hotel Booking")
        print("11. Delete Train Booking (Admin)")
        print("12. Delete Flight Booking (Admin)")
        print("13. Delete Hotel Booking (Admin)")
        print("14. Update Train Travel Date (Admin)")
        print("0. Exit")

        choice = input("Enter choice: ")
        if choice == "1": seed_schedules()
        elif choice == "2": view_schedule("train_schedule")
        elif choice == "3": view_schedule("flight_schedule")
        elif choice == "4": view_schedule("hotel_schedule")
        elif choice == "5": book_train()
        elif choice == "6": book_flight()
        elif choice == "7": book_hotel()
        elif choice == "8": search_booking("railway_bookings", "train_schedule", "id", ["id", "name", "train_id", "travel_date"])
        elif choice == "9": search_booking("airline_bookings", "flight_schedule", "id", ["id", "name", "flight_id", "travel_date"])
        elif choice == "10": search_booking("hotel_bookings", "hotel_schedule", "id", ["id", "name", "hotel_id"])
        elif choice == "11": delete_booking("railway_bookings")
        elif choice == "12": delete_booking("airline_bookings")
        elif choice == "13": delete_booking("hotel_bookings")
        elif choice == "14": update_train_date()
        elif choice == "0":
            print("👋 Exiting...")
            break
        else:
            print("⚠️ Invalid option.")

main_menu()
conn.close()
