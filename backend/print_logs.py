import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    cur.execute("SELECT channel, recipient, status, created_at, message FROM notification_logs ORDER BY id DESC LIMIT 4")
    print("LATEST CARRIER NOTIFICATION AUDIT TRAIL:")
    for r in cur.fetchall():
        clean_msg = r["message"].encode("ascii", "replace").decode("ascii")
        print(f" * [{r['channel']}] -> {r['recipient']} | Status: {r['status']} | Time: {r['created_at']}")
        print(f"   {clean_msg[:90]}...\n")
