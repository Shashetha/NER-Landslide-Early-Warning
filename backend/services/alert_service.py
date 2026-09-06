import logging
from typing import List, Optional

from database import get_db
from schemas.alert import AlertResponse

logger = logging.getLogger(__name__)


class AlertService:
    async def get_all_alerts(
        self,
        status: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> List[AlertResponse]:
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if status:
            query += " AND status = %s"
            params.append(status)
        if risk_level:
            query += " AND risk_level = %s"
            params.append(risk_level.upper())

        query += " ORDER BY created_at DESC"

        with get_db() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        return [
            AlertResponse(
                id=r["id"],
                location=r["location"],
                latitude=float(r["latitude"]),
                longitude=float(r["longitude"]),
                risk_level=r["risk_level"],
                probability=float(r["probability"]),
                status=r["status"],
                affected_population=r["affected_population"],
                description=r["description"],
                created_at=r["created_at"].isoformat() + "Z",
                updated_at=r["updated_at"].isoformat() + "Z",
            )
            for r in rows
        ]

    async def get_alert_by_id(self, alert_id: int) -> Optional[AlertResponse]:
        with get_db() as cur:
            cur.execute("SELECT * FROM alerts WHERE id = %s", (alert_id,))
            row = cur.fetchone()

        if not row:
            return None

        return AlertResponse(
            id=row["id"],
            location=row["location"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            risk_level=row["risk_level"],
            probability=float(row["probability"]),
            status=row["status"],
            affected_population=row["affected_population"],
            description=row["description"],
            created_at=row["created_at"].isoformat() + "Z",
            updated_at=row["updated_at"].isoformat() + "Z",
        )

    async def create_alert(
        self,
        location: str,
        latitude: float,
        longitude: float,
        risk_level: str,
        probability: float,
        affected_population: int,
        description: str,
        status: str = "active",
    ) -> AlertResponse:
        sql = """
            INSERT INTO alerts
                (location, latitude, longitude, risk_level, probability,
                 status, affected_population, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_db() as cur:
            cur.execute(sql, (
                location, latitude, longitude, risk_level.upper(),
                probability, status, affected_population, description,
            ))
            new_id = cur.lastrowid
            cur.execute("SELECT * FROM alerts WHERE id = %s", (new_id,))
            row = cur.fetchone()

        return AlertResponse(
            id=row["id"],
            location=row["location"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            risk_level=row["risk_level"],
            probability=float(row["probability"]),
            status=row["status"],
            affected_population=row["affected_population"],
            description=row["description"],
            created_at=row["created_at"].isoformat() + "Z",
            updated_at=row["updated_at"].isoformat() + "Z",
        )


alert_service = AlertService()
