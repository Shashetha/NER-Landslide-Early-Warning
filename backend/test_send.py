import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from providers.notifications import sms_provider

async def send_test():
    phone = "918778339906"
    print(f"Triggering direct carrier dispatch to {phone}...")
    res = await sms_provider.send_sms(phone, "LANDSLIDE ALERT: Immediate slope failure hazard at Gangtok. Stay alert.")
    print("Carrier Gateway Response:", res)

if __name__ == "__main__":
    asyncio.run(send_test())
