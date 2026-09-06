import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from providers.notifications import sms_provider

async def send_direct_sms():
    phone = "8778339906"
    msg = "GOVT DISASTER ALERT: [CRITICAL RISK (92%)] Landslide threat detected at Gangtok (NH10 Corridor), Sikkim. Immediate evacuation advised."
    print(f"Sending real SMS to {phone} via Fast2SMS...")
    res = await sms_provider.send_sms(phone, msg)
    print("Fast2SMS Response:", res)

if __name__ == "__main__":
    asyncio.run(send_direct_sms())
