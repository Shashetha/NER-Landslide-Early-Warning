import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from providers.notifications import sms_provider

async def send_fresh_sms():
    phone = "+918778339906"
    msg = "GOVT DISASTER ALERT: [CRITICAL RISK (96%)] Landslide threat detected at Mangan, North Sikkim. Immediate evacuation advised."
    print(f"Sending fresh emergency SMS to {phone} via TextBee...")
    res = await sms_provider.send_sms(phone, msg)
    print("TextBee Result:", res)

if __name__ == "__main__":
    asyncio.run(send_fresh_sms())
