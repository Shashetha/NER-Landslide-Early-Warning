import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.auth_service import hash_password

database.init_pool()

my_phone = "+918778339906"
my_email = "rithish@ner-disaster.gov.in"
hashed_pwd = hash_password("admin123")

with database.get_db() as cur:
    # 1. Update existing Admin and Officer phone numbers to your phone
    cur.execute("UPDATE users SET phone_number = %s WHERE id IN (1, 2)", (my_phone,))

    # 2. Insert Rithish as Lead Disaster Commander across all 8 NER States
    cur.execute("SELECT id FROM users WHERE phone_number = %s AND email = %s", (my_phone, my_email))
    existing = cur.fetchone()
    if not existing:
        cur.execute(
            """
            INSERT INTO users (email, hashed_password, full_name, phone_number, role, state, district)
            VALUES (%s, %s, %s, %s, %s, NULL, 'Regional Command')
            """,
            (my_email, hashed_pwd, "Rithish (Lead Disaster Response Officer)", my_phone, "ADMIN")
        )

    print(f"SUCCESS: Phone number {my_phone} registered across all emergency alert broadcasts.")

    cur.execute("SELECT id, full_name, role, phone_number, state FROM users")
    print("\nUpdated User Broadcast Table:")
    for u in cur.fetchall():
        print(f" * [{u['role']}] {u['full_name']} | Phone: {u['phone_number']} | State: {u['state'] or 'ALL (Global)'}")
