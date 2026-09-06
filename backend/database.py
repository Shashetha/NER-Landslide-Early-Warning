import os
import logging
from contextlib import contextmanager

import mysql.connector
from mysql.connector import pooling

logger = logging.getLogger(__name__)

_pool: pooling.MySQLConnectionPool | None = None


def init_pool() -> None:
    global _pool
    config = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "landslide_db"),
        "pool_name": "landslide_pool",
        "pool_size": int(os.getenv("DB_POOL_SIZE", 5)),
        "autocommit": False,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "use_unicode": True,
    }
    try:
        _pool = pooling.MySQLConnectionPool(**config)
        logger.info(
            "MySQL connection pool created → %s:%s/%s",
            config["host"], config["port"], config["database"],
        )
    except Exception as exc:
        logger.error("Failed to create MySQL pool: %s", exc)
        raise


@contextmanager
def get_db():
    if _pool is None:
        raise RuntimeError("Database pool is not initialised. Call init_pool() first.")
    conn = _pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def init_schema() -> None:
    schema_path = os.path.join(os.path.dirname(__file__), "db", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    statements = [s.strip() for s in sql.split(";") if s.strip()]
    with get_db() as cur:
        for stmt in statements:
            cur.execute(stmt)
    logger.info("Database schema initialised")
