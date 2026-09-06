import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from providers.notifications import sms_provider

NEARBY_PEOPLE = [
    "+918939731732",
    "+919094686461",
    "+919176456494",
    "+918940627897",
    "+917338761573",
]

MSG = (
    "GOVT DISASTER ALERT: [CRITICAL RISK (96%)] Landslide hazard detected at Gangtok (NH-10 Highway Corridor), Sikkim. "
    "Stay away from steep hill slopes. Follow local emergency advisories. - NER Early Warning System"
)

async def send_to_all():
    print(f"Dispatching emergency SMS to {len(NEARBY_PEOPLE)} nearby people via TextBee...\n")
    for number in NEARBY_PEOPLE:
        res = await sms_provider.send_sms(number, MSG)
        status = "DELIVERED" if res.get("success") else "FAILED"
        print(f" * {number} -> {status}  |  Batch ID: {res.get('batch_id', res.get('error', 'N/A'))}")
    print("\nAll dispatches completed.")

if __name__ == "__main__":
    asyncio.run(send_to_all())
