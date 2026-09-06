import logging
import asyncio
from typing import List, Optional
from datetime import datetime

import database
from schemas.alert import AlertResponse
from data.ner_locations import NER_MONITORED_LOCATIONS
from services.prediction_service import prediction_service
from providers.open_meteo import multi_hazard_provider, rainfall_provider, soil_moisture_provider

logger = logging.getLogger(__name__)


class AlertService:
    async def get_all_alerts(
        self,
        status: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> List[AlertResponse]:
        """Fetch alerts from database, ordered by severity and time."""
        if database._pool is None:
            return []

        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if status:
            query += " AND status = %s"
            params.append(status)
        if risk_level:
            query += " AND risk_level = %s"
            params.append(risk_level.upper())

        query += " ORDER BY CASE risk_level WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END, updated_at DESC"

        with database.get_db() as cur:
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
        if database._pool is None:
            return None

        with database.get_db() as cur:
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

    async def sync_live_alerts_from_ml(self) -> dict:
        """
        Runs batch ML risk evaluation across all 40 monitored stations using live weather telemetry,
        and updates the alerts database.
        """
        logger.info("Executing batch ML risk evaluation for %d NER monitored locations...", len(NER_MONITORED_LOCATIONS))

        coords = [(loc["latitude"], loc["longitude"]) for loc in NER_MONITORED_LOCATIONS]

        # 1. Fetch batched environmental data
        rain_batch, sm_batch = await asyncio.gather(
            rainfall_provider.get_batch(coords),
            soil_moisture_provider.get_batch(coords),
        )

        valid_results = []
        for i, loc in enumerate(NER_MONITORED_LOCATIONS):
            r = rain_batch[i] if i < len(rain_batch) else {}
            sm = sm_batch[i] if i < len(sm_batch) else None

            try:
                pred = await prediction_service.predict_landslide_risk(
                    latitude=loc["latitude"],
                    longitude=loc["longitude"],
                    rainfall_1d=r.get("rainfall_1d"),
                    rainfall_3d=r.get("rainfall_3d"),
                    rainfall_7d=r.get("rainfall_7d"),
                    elevation_m=loc.get("elevation_m"),
                    slope_degrees=loc.get("slope_degrees"),
                    soil_moisture=sm,
                )
                
                loc_name = f"{loc['name']}, {loc['state']}"

                valid_results.append({
                    "location": loc_name,
                    "latitude": loc["latitude"],
                    "longitude": loc["longitude"],
                    "risk_level": pred.risk_level,
                    "probability": pred.probability,
                    "affected_population": loc.get("population", 5000),
                    "description": pred.explanation,
                    "status": "active" if pred.risk_level in ("HIGH", "CRITICAL") else ("monitoring" if pred.risk_level == "MEDIUM" else "resolved"),
                })
            except Exception as e:
                logger.error("Failed to predict for %s: %s", loc['name'], e)

        # 2. Update alerts in database
        if database._pool is not None and valid_results:
            with database.get_db() as cur:
                for item in valid_results:
                    cur.execute("SELECT id FROM alerts WHERE location = %s LIMIT 1", (item["location"],))
                    existing = cur.fetchone()
                    if existing:
                        sql = """
                            UPDATE alerts
                            SET risk_level = %s, probability = %s, status = %s,
                                description = %s, updated_at = NOW()
                            WHERE id = %s
                        """
                        cur.execute(sql, (
                            item["risk_level"], item["probability"], item["status"],
                            item["description"], existing["id"]
                        ))
                    else:
                        sql = """
                            INSERT INTO alerts
                                (location, latitude, longitude, risk_level, probability,
                                 status, affected_population, description, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        """
                        cur.execute(sql, (
                            item["location"], item["latitude"], item["longitude"],
                            item["risk_level"], item["probability"], item["status"],
                            item["affected_population"], item["description"]
                        ))

        logger.info("Successfully updated %d stations via live ML model inference", len(valid_results))
        return {
            "total_evaluated": len(valid_results),
            "critical": sum(1 for r in valid_results if r["risk_level"] == "CRITICAL"),
            "high": sum(1 for r in valid_results if r["risk_level"] == "HIGH"),
            "medium": sum(1 for r in valid_results if r["risk_level"] == "MEDIUM"),
            "low": sum(1 for r in valid_results if r["risk_level"] == "LOW"),
        }

    async def get_regional_dashboard_summary(self) -> dict:
        """
        Returns real-time regional dashboard statistics calculated strictly from:
        1. Live alerts table in MySQL
        2. Real count of hazard reports filed today from MySQL
        3. Real Open-Meteo precipitation history
        """
        alerts = await self.get_all_alerts()

        dist = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        active_alerts_count = 0
        high_risk_areas_count = 0

        for a in alerts:
            lvl = a.risk_level.lower()
            if lvl in dist:
                dist[lvl] += 1
            if a.status == "active":
                active_alerts_count += 1
            if a.risk_level in ("HIGH", "CRITICAL"):
                high_risk_areas_count += 1

        # Query real count of field reports filed today from database
        reports_today = 0
        if database._pool is not None:
            try:
                with database.get_db() as cur:
                    cur.execute("SELECT COUNT(*) as cnt FROM hazard_reports WHERE DATE(created_at) = CURDATE()")
                    row = cur.fetchone()
                    reports_today = row["cnt"] if row else 0
            except Exception:
                reports_today = 0

        # Query real telemetry for regional precipitation history (Shillong Central NER Plateau)
        w_data = await multi_hazard_provider.get_full_weather_forecast(25.5788, 91.8933)
        past_precip = w_data.get("past_daily_precip", [])
        
        days_labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Today"]
        rainfall_trend = []
        if len(past_precip) >= 7:
            for i, p in enumerate(past_precip[-7:]):
                rainfall_trend.append({"day": days_labels[i], "rainfall": round(float(p), 1)})
        else:
            for i, d in enumerate(days_labels):
                rainfall_trend.append({"day": d, "rainfall": 0.0})

        r7d_sum = sum(p["rainfall"] for p in rainfall_trend)
        daily_avg = round(r7d_sum / max(len(rainfall_trend), 1), 1)

        return {
            "statistics": {
                "monitoredLocations": len(NER_MONITORED_LOCATIONS),
                "highRiskAreas": high_risk_areas_count,
                "activeAlerts": active_alerts_count,
                "reportsToday": reports_today,
            },
            "riskDistribution": dist,
            "rainfallData": {
                "last7Days": rainfall_trend,
                "total7dRainfall": round(r7d_sum, 1),
                "dailyAverage": daily_avg,
            },
            "recentAlerts": [
                {
                    "id": a.id,
                    "location": a.location,
                    "riskLevel": a.risk_level,
                    "probability": a.probability,
                    "latitude": a.latitude,
                    "longitude": a.longitude,
                    "status": a.status,
                    "timestamp": a.updated_at,
                }
                for a in alerts[:10]
            ],
        }

    async def get_all_risk_zones(self) -> List[dict]:
        """Return map zones for all monitored NER stations with live ML risk levels."""
        alerts = await self.get_all_alerts()
        alerts_map = {a.location.lower().strip(): a for a in alerts}

        zones = []
        for loc in NER_MONITORED_LOCATIONS:
            key = f"{loc['name']}, {loc['state']}".lower().strip()
            alert = alerts_map.get(key)
            risk_level = alert.risk_level if alert else "LOW"
            prob = alert.probability if alert else 0.28

            radius = 3500 if risk_level == "CRITICAL" else (2500 if risk_level == "HIGH" else (1800 if risk_level == "MEDIUM" else 1200))

            zones.append({
                "id": f"zone_{loc['id']}",
                "name": f"{loc['name']}, {loc['state']}",
                "state": loc["state"],
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "elevation_m": loc.get("elevation_m"),
                "slope_degrees": loc.get("slope_degrees"),
                "riskLevel": risk_level,
                "probability": prob,
                "radius": radius,
            })
        return zones


alert_service = AlertService()
