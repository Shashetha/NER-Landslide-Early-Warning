import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.notification_service import notification_service


async def main():
    database.init_pool()
    print("Testing Automated Multi-Channel Emergency Broadcast...")

    res = await notification_service.broadcast_landslide_warning(
        alert_id=2,
        location="Cherrapunji, Meghalaya",
        risk_level="CRITICAL",
        probability=0.96,
        description="Over 350mm precipitation recorded with severe slope destabilization.",
        state="Meghalaya",
    )
    print("Broadcast Dispatch Summary:", res)

    logs = await notification_service.get_notification_logs(limit=6)
    print("\nAudit Logs in MySQL:")
    for l in logs:
        print(f"  * [{l['channel']}] -> {l['recipient']} ({l['recipient_role']}) | Status: {l['status']}")


if __name__ == "__main__":
    asyncio.run(main())
