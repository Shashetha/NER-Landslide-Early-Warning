import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from services.prediction_service import prediction_service

async def test_forecast():
    lat = 27.3389  # Gangtok, Sikkim
    lng = 88.6065
    print(f"Executing Future Multi-Hazard Risk Forecast for Gangtok ({lat}, {lng})...\n")

    res = await prediction_service.predict_multi_hazard_forecast(lat, lng)

    print("==================================================================")
    print("FUTURE MULTI-HAZARD FORECAST (24h, 48h, 72h, 7-DAY TIMELINE)")
    print("==================================================================")
    print(f"Location: ({res.latitude}, {res.longitude}) | Elev: {res.elevation_m}m | Slope: {res.slope_degrees}°")
    print(f"Summary Advisory: {res.summary_advisory}\n")

    print("--- 7-Day Rolling Hazard Timeline ---")
    for w in res.timeline_7d:
        print(f" * {w.horizon:12s} ({w.date_label:10s}) | Rain: {w.rainfall_surge_mm:4.1f}mm | Soil: {w.soil_moisture_pct:4.1f}% | Landslide: {w.landslide_risk_level:8s} ({int(w.landslide_probability*100):2d}%) | Flood: {w.flash_flood_risk:8s}")

if __name__ == "__main__":
    asyncio.run(test_forecast())
