import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

citizens = [
    ("Citizen 1 (Sikkim North)", "+918939731732", "Sikkim", "North Sikkim"),
    ("Citizen 2 (Sikkim East)", "+919094686461", "Sikkim", "East Sikkim"),
    ("Citizen 3 (Sikkim South)", "+919176456494", "Sikkim", "South Sikkim"),
    ("Citizen 4 (Sikkim West)", "+918940627897", "Sikkim", "West Sikkim"),
    ("Citizen 5 (Gangtok Corridor)", "+917338761573", "Sikkim", "East Sikkim"),
]

with database.get_db() as cur:
    for name, phone, state, district in citizens:
        dummy_email = f"user_{phone.replace('+', '')}@ner-alerts.in"
        cur.execute("SELECT id FROM users WHERE phone_number = %s", (phone,))
        existing = cur.fetchone()
        if existing:
            cur.execute(
                "UPDATE users SET full_name = %s, state = %s, district = %s, is_active = TRUE WHERE id = %s",
                (name, state, district, existing["id"])
            )
        else:
            cur.execute(
                """
                INSERT INTO users (email, hashed_password, full_name, phone_number, role, state, district, is_active)
                VALUES (%s, 'OFFLINE_PASS', %s, %s, 'CITIZEN', %s, %s, TRUE)
                """,
                (dummy_email, name, phone, state, district)
            )

    print("SUCCESS: 5 nearby citizens registered in MySQL database.")
    cur.execute("SELECT id, full_name, phone_number, role, state FROM users WHERE phone_number IN (%s, %s, %s, %s, %s)", tuple(c[1] for c in citizens))
    for u in cur.fetchall():
        print(f" * [{u['role']}] {u['full_name']} | Phone: {u['phone_number']} | State: {u['state']}")
