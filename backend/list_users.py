import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    cur.execute("SELECT id, full_name, email, phone_number, role, state, district FROM users")
    print("ALL REGISTERED USERS IN DATABASE:")
    for u in cur.fetchall():
        print(f" * [{u['role']}] {u['full_name']} | State: {u['state']} | Phone: {u['phone_number']} | Email: {u['email']}")
