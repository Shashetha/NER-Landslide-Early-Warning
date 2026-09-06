import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.notification_service import notification_service

async def verify_carrier_sms():
    database.init_pool()
    phone = "918778339906"

    print(f"1. Sending Real Carrier Landslide Alert to {phone} via MSG91...")
    res = await notification_service.broadcast_landslide_warning(
        alert_id=999,
        location="Gangtok, Sikkim",
        risk_level="CRITICAL",
        probability=0.96,
        description="Over 380mm rainfall & active slope fissures detected by AI telemetry. Evacuate immediately.",
        state="Sikkim"
    )

    print("\nBroadcast Result:", res)

if __name__ == "__main__":
    asyncio.run(verify_carrier_sms())
