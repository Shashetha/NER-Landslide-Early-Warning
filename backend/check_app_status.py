import os
import sys
import asyncio
import httpx

api_key = "txb_lsIM6PBLPH0A3Olz6a66ID1rDHugqBBa"
device_id = "6a9d535bccb6c72709b03d60"

async def check_app_status():
    headers = {"x-api-key": api_key}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}", headers=headers)
        data = r.json().get("data", {})
        print("Device Online:", data.get("enabled"))
        print("Model:", data.get("model"))
        print("Last Heartbeat:", data.get("lastHeartbeat"))
        print("Sent SMS Count:", data.get("sentSMSCount"))
        print("Battery:", data.get("batteryInfo", {}).get("percentage"), "%")

if __name__ == "__main__":
    asyncio.run(check_app_status())
