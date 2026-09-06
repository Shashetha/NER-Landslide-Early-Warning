import os
import sys
import asyncio
import httpx

api_key = "txb_lsIM6PBLPH0A3Olz6a66ID1rDHugqBBa"
device_id = "6a9d535bccb6c72709b03d60"

async def diagnose_textbee():
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        print("1. Fetching TextBee Device Telemetry...")
        r_dev = await client.get(f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}", headers=headers)
        data = r_dev.json().get("data", {})
        print(f"Device: {data.get('name')} | Enabled: {data.get('enabled')} | App Version: {data.get('appVersionName')}")
        print(f"Heartbeat: {data.get('lastHeartbeat')}")
        print(f"Total Sent SMS count reported by device: {data.get('sentSMSCount')}")

        print("\n2. Pushing Direct Test SMS via TextBee...")
        payload = {
            "recipients": ["+918778339906"],
            "message": "NER DISASTER ALERT: Test verification SMS from TextBee Gateway."
        }
        r_sms = await client.post(f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}/send-sms", headers=headers, json=payload)
        print("API Response Code:", r_sms.status_code)
        print("API Response Body:", r_sms.text)

if __name__ == "__main__":
    asyncio.run(diagnose_textbee())
