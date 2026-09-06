import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.proximity_alert_service import proximity_alert_service

async def test_proximity():
    database.init_pool()
    print("Testing Proximity-Based SMS Dispatch (Targeting people within 50km of Gangtok)...")

    res = await proximity_alert_service.broadcast_to_nearby_people(
        location_name="Gangtok (NH-10 Highway Corridor), Sikkim",
        hazard_lat=27.3389,
        hazard_lng=88.6065,
        risk_level="CRITICAL",
        probability=0.96,
        description="Active slope fissures & 390mm rainfall detected by AI telemetry.",
        radius_km=50.0,
        state="Sikkim"
    )

    print("\nProximity Dispatch Result:", res)

if __name__ == "__main__":
    asyncio.run(test_proximity())
