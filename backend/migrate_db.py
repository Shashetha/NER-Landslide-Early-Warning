import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

database.init_pool()

with database.get_db() as cur:
    cur.execute("SHOW COLUMNS FROM hazard_reports")
    cols = [r["Field"] for r in cur.fetchall()]

    add_cols = [
        ("user_id", "INT"),
        ("reporter_name", "VARCHAR(255)"),
        ("state", "VARCHAR(100)"),
        ("district", "VARCHAR(100)"),
        ("visible_cracks", "BOOLEAN NOT NULL DEFAULT FALSE"),
        ("rockfall_observed", "BOOLEAN NOT NULL DEFAULT FALSE"),
        ("road_blocked", "BOOLEAN NOT NULL DEFAULT FALSE"),
        ("water_accumulation", "BOOLEAN NOT NULL DEFAULT FALSE"),
        ("soil_movement", "BOOLEAN NOT NULL DEFAULT FALSE"),
        ("media_url", "VARCHAR(512)"),
        ("admin_notes", "TEXT"),
        ("idempotency_key", "VARCHAR(128)"),
        ("sync_status", "VARCHAR(32) DEFAULT 'SYNCED'"),
        ("updated_at", "DATETIME ON UPDATE CURRENT_TIMESTAMP"),
    ]
    for col_name, col_type in add_cols:
        if col_name not in cols:
            cur.execute(f"ALTER TABLE hazard_reports ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")

print("Table migration successful.")
