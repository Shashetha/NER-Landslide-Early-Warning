import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    cur.execute("DELETE FROM users WHERE full_name = 'string' OR phone_number = 'string'")
    print("Cleaned dummy placeholder test entries.")

    cur.execute("SELECT id, full_name, role, phone_number, state FROM users ORDER BY id ASC")
    print("\nFINAL REGISTERED USERS (STRICTLY UNIQUE):")
    for u in cur.fetchall():
        print(f" * [{u['role']}] {u['full_name']} | Phone: {u['phone_number']} | State: {u['state']}")
