import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.auth_service import hash_password, verify_password

database.init_pool()

target_email = "m.rithish1882007@gmail.com"
plain_pwd = "admin123"
fresh_hash = hash_password(plain_pwd)

with database.get_db() as cur:
    cur.execute("SELECT id, email, hashed_password FROM users WHERE email = %s", (target_email,))
    user = cur.fetchone()
    print("User in DB before update:", user)

    # Force update the password hash
    cur.execute("UPDATE users SET hashed_password = %s WHERE email = %s", (fresh_hash, target_email))
    
    # Also update admin fallback email
    cur.execute("UPDATE users SET hashed_password = %s WHERE email = %s", (fresh_hash, "admin@ner-disaster.gov.in"))

    # Test verify
    cur.execute("SELECT email, hashed_password FROM users WHERE email = %s", (target_email,))
    updated_user = cur.fetchone()
    is_valid = verify_password(plain_pwd, updated_user["hashed_password"])
    print(f"Verification test for '{target_email}' with '{plain_pwd}':", "VALID" if is_valid else "FAILED")
