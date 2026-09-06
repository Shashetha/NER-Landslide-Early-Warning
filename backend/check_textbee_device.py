import os
import sys
import asyncio
import httpx

api_key = "txb_lsIM6PBLPH0A3Olz6a66ID1rDHugqBBa"
device_id = "6a9d535bccb6c72709b03d60"

async def check_device_status():
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Check device status
        print("1. Checking Device connection on TextBee...")
        r_dev = await client.get(f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}", headers=headers)
        print("Device Status:", r_dev.status_code, r_dev.text)

        # Check pending SMS queue for this device
        print("\n2. Checking SMS outbox queue...")
        r_logs = await client.get(f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}/outbox", headers=headers)
        print("Outbox Status:", r_logs.status_code, r_logs.text[:400])

if __name__ == "__main__":
    asyncio.run(check_device_status())
