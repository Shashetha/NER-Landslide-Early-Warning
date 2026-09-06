import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

my_phone = "+918778339906"
my_email = "m.rithish1882007@gmail.com"

with database.get_db() as cur:
    # 1. Update the record for ID 1 to your email and phone
    cur.execute("UPDATE users SET email = %s, phone_number = %s, full_name = 'Rithish (Lead Disaster Response Officer)' WHERE id = 1", (my_email, my_phone))
    
    # 2. Update officer ID 2 phone
    cur.execute("UPDATE users SET phone_number = %s WHERE id = 2", (my_phone,))

    print(f"SUCCESS: Email {my_email} and Phone {my_phone} linked.")

    cur.execute("SELECT id, full_name, role, phone_number, email, state FROM users")
    print("\nUpdated User Broadcast Registry in MySQL:")
    for u in cur.fetchall():
        print(f" * [{u['role']}] {u['full_name']} | Phone: {u['phone_number']} | Email: {u['email']} | State: {u['state'] or 'ALL (Global)'}")
