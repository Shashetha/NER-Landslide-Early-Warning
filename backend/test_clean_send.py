import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from providers.notifications import sms_provider

async def send_live_verification():
    phone = "+918778339906"
    msg = "GOVT DISASTER ALERT: [CRITICAL RISK (96%)] Imminent landslide hazard detected at Gangtok, Sikkim. Evacuate immediately."
    print(f"Sending live SMS through TextBee to {phone}...")
    res = await sms_provider.send_sms(phone, msg)
    print("Live Gateway Result:", res)

if __name__ == "__main__":
    asyncio.run(send_live_verification())
