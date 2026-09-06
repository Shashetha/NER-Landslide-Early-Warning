import os
import sys
import asyncio
import httpx

api_key = "txb_lsIM6PBLPH0A3Olz6a66ID1rDHugqBBa"
device_id = "6a9d535bccb6c72709b03d60"
phone_number = "+918778339906"
message = "GOVT DISASTER ALERT: [CRITICAL RISK (94%)] Landslide threat detected at Gangtok (NH-10 Highway Corridor), Sikkim. Immediate evacuation advised."

async def test_textbee():
    print(f"Testing TextBee Gateway for Device: {device_id}...")

    url = f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}/send-sms"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "recipients": [phone_number],
        "message": message
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            print("Status Code:", resp.status_code)
            print("Response:", resp.text)
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    asyncio.run(test_textbee())
