from fastapi import APIRouter, Query
from typing import Optional, Dict, Any
from services.gis_service import gis_service

router = APIRouter()


@router.get("/risk-map")
async def get_risk_map_points(
    state: Optional[str] = Query(None, description="Filter by NER State"),
    min_probability: Optional[float] = Query(0.0, description="Filter by minimum risk probability")
):
    """
    Standard Real-Time GIS Risk Map Endpoint:
    Returns clean point coordinates, ML probability, risk level, rainfall, elevation, slope, and soil moisture.
    Format: latitude, longitude, risk_probability, risk_level, timestamp
    """
    zones_res = await gis_service.get_risk_zones_geojson(state=state)
    features = zones_res.get("features", [])

    points = []
    for f in features:
        props = f["properties"]
        coords = f["geometry"]["coordinates"]
        prob = float(props.get("probability", 0.3))

        if prob >= min_probability:
            points.append({
                "id": props.get("id"),
                "name": props.get("name"),
                "state": props.get("state"),
                "type": props.get("type", "LIVE_MONITORING_STATION"),
                "latitude": coords[1],
                "longitude": coords[0],
                "risk_probability": round(prob, 4),
                "risk_level": props.get("risk_level", "LOW"),
                "rainfall_7d": props.get("rainfall_7d"),
                "elevation_m": props.get("elevation_m"),
                "slope_degrees": props.get("slope_degrees"),
                "soil_moisture": props.get("soil_moisture", 0.34),
                "timestamp": props.get("updated_at") or "2026-09-06T15:00:00Z"
            })

    return {
        "region": "North Eastern Region (NER), India",
        "total_points": len(points),
        "data": points
    }


@router.get("/gis/risk-zones")
async def get_risk_zones_geojson(
    state: Optional[str] = Query(None, description="Filter by NER state (e.g. Sikkim, Meghalaya)"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level (LOW, MEDIUM, HIGH, CRITICAL)")
):
    return await gis_service.get_risk_zones_geojson(state=state, risk_level=risk_level)


@router.get("/gis/heatmap")
async def get_risk_heatmap(
    state: Optional[str] = Query(None, description="Filter by NER state"),
    min_risk: Optional[str] = Query(None, description="Minimum risk threshold filter")
):
    return await gis_service.get_risk_heatmap_points(state=state, min_risk=min_risk)


@router.get("/gis/regions")
async def get_regions():
    return await gis_service.get_administrative_regions()
