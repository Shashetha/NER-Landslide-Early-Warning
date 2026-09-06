import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database
from services.notification_service import notification_service

async def test_email_and_sms():
    database.init_pool()

    print("==================================================================")
    print("SENDING TEST EMERGENCY BROADCAST TO YOUR REGISTERED CONTACTS")
    print("==================================================================")

    res = await notification_service.broadcast_landslide_warning(
        alert_id=202,
        location="Mangan District, North Sikkim",
        risk_level="CRITICAL",
        probability=0.96,
        description="Active ground fissures and 420mm 7-day cumulative rainfall detected by AI telemetry. Slope failure imminent.",
        state="Sikkim"
    )

    print("\nDispatch Summary:", res)

    print("\nNotification Audit Logs in MySQL:")
    logs = await notification_service.get_notification_logs(limit=4)
    for l in logs:
        clean_msg = l['message'].encode('ascii', 'replace').decode('ascii')
        print(f" * [{l['channel']}] -> {l['recipient']} ({l['recipient_role']}) | Status: {l['status']}")

if __name__ == "__main__":
    asyncio.run(test_email_and_sms())
