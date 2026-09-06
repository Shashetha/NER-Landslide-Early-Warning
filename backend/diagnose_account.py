import os
import sys
import asyncio
import httpx

auth_key = "568268AYnishnksQ76a9d47c4P1"
phone = "918778339906"

async def diagnose_msg91():
    headers = {"authkey": auth_key}
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Check sender IDs approved on this MSG91 account
        print("1. Checking approved Sender IDs on MSG91 account...")
        r_sender = await client.get("https://control.msg91.com/api/v5/sender/all", headers=headers)
        print("Sender IDs:", r_sender.status_code, r_sender.text)

        # Check templates on MSG91 account
        print("\n2. Checking approved Flow Templates...")
        r_flow = await client.get("https://control.msg91.com/api/v5/flow/", headers=headers)
        print("Templates:", r_flow.status_code, r_flow.text)

if __name__ == "__main__":
    asyncio.run(diagnose_msg91())
