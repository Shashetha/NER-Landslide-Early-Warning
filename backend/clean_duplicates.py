import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    print("--- 1. AUDITING AND CLEANING USERS TABLE ---")
    cur.execute("SELECT id, full_name, email, phone_number, role, state FROM users ORDER BY id ASC")
    all_users = cur.fetchall()
    
    seen_phones = set()
    user_ids_to_keep = []
    user_ids_to_delete = []

    for u in all_users:
        phone = u.get("phone_number")
        if not phone or phone in seen_phones:
            user_ids_to_delete.append(u["id"])
        else:
            seen_phones.add(phone)
            user_ids_to_keep.append(u["id"])

    if user_ids_to_delete:
        format_strings = ','.join(['%s'] * len(user_ids_to_delete))
        cur.execute(f"DELETE FROM users WHERE id IN ({format_strings})", tuple(user_ids_to_delete))
        print(f"Removed {len(user_ids_to_delete)} duplicate user records.")

    print("\n--- 2. AUDITING AND CLEANING ALERTS TABLE ---")
    cur.execute("SELECT id, location, latitude, longitude FROM alerts ORDER BY id ASC")
    all_alerts = cur.fetchall()

    seen_locs = set()
    alert_ids_to_delete = []
    for a in all_alerts:
        loc_key = a["location"].strip().lower()
        if loc_key in seen_locs:
            alert_ids_to_delete.append(a["id"])
        else:
            seen_locs.add(loc_key)

    if alert_ids_to_delete:
        format_strings = ','.join(['%s'] * len(alert_ids_to_delete))
        cur.execute(f"DELETE FROM alerts WHERE id IN ({format_strings})", tuple(alert_ids_to_delete))
        print(f"Removed {len(alert_ids_to_delete)} duplicate alert records.")

    print("\n--- 3. CLEANED REGISTERED USERS (NO DUPLICATES) ---")
    cur.execute("SELECT id, full_name, role, phone_number, state FROM users ORDER BY id ASC")
    for u in cur.fetchall():
        print(f" * ID {u['id']}: [{u['role']}] {u['full_name']} | Phone: {u['phone_number']} | State: {u['state'] or 'ALL'}")

    print("\n--- 4. CLEANED ACTIVE ALERTS COUNT ---")
    cur.execute("SELECT COUNT(*) as total FROM alerts")
    print(f"Total Unique Monitored Stations in Alerts Table: {cur.fetchone()['total']}")
