import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    cur.execute("SELECT id, channel, recipient, status, created_at, message FROM notification_logs ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    print("DATABASE NOTIFICATION AUDIT TRAIL:")
    for r in rows:
        print(f" * [{r['channel']}] to {r['recipient']} -> {r['status']} at {r['created_at']}")
        print(f"   {r['message'][:80]}...\n")
