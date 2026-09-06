import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.notification_service import notification_service

async def test_hackathon_broadcast():
    database.init_pool()

    print("==================================================================")
    print("HACKATHON LIVE DEMO: DISPATCHING EMERGENCY LANDSLIDE EARLY WARNING")
    print("==================================================================")

    res = await notification_service.broadcast_landslide_warning(
        alert_id=101,
        location="Gangtok (NH-10 Highway Corridor), Sikkim",
        risk_level="CRITICAL",
        probability=0.94,
        description="Continuous heavy monsoon precipitation (380mm in 7 days) and saturated slope fissures detected by AI telemetry.",
        state="Sikkim"
    )

    print("\nDispatch Summary:", res)

    print("\nRecent Notification Audit Trail in MySQL:")
    logs = await notification_service.get_notification_logs(limit=4)
    for l in logs:
        # Strip high unicode for windows console printing
        clean_msg = l['message'].encode('ascii', 'replace').decode('ascii')
        print(f" * [{l['channel']}] -> {l['recipient']} ({l['recipient_role']}) | Status: {l['status']}")
        print(f"   Message: {clean_msg[:100]}...\n")

if __name__ == "__main__":
    asyncio.run(test_hackathon_broadcast())
