import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.notification_service import notification_service

async def run_end_to_end_sms():
    database.init_pool()
    print("Executing End-to-End Emergency Dispatch through TextBee...")

    res = await notification_service.broadcast_landslide_warning(
        alert_id=888,
        location="Gangtok, Sikkim",
        risk_level="CRITICAL",
        probability=0.96,
        description="Heavy monsoon precipitation (390mm) and active slope fissures detected.",
        state="Sikkim"
    )

    print("\nDispatch Result:", res)

if __name__ == "__main__":
    asyncio.run(run_end_to_end_sms())
