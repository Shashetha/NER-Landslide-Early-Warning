import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    cur.execute("SELECT id, location, risk_level, probability, description, updated_at FROM alerts ORDER BY updated_at DESC LIMIT 6")
    print("VERIFIED LIVE ML ALERTS IN MYSQL DATABASE:")
    for a in cur.fetchall():
        clean_desc = a["description"].encode("ascii", "replace").decode("ascii")
        print(f" * [{a['risk_level']}] {a['location']} (Prob: {int(a['probability']*100)}%)")
        print(f"   {clean_desc[:85]}...\n")
