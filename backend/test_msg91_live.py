import os
import sys
import asyncio
import httpx

auth_key = "568268AYnishnksQ76a9d47c4P1"
phone_number = "918778339906"
message = "GOVT DISASTER ALERT: [CRITICAL RISK (94%)] Landslide threat detected at Gangtok, Sikkim. Avoid unstable slopes and follow local disaster advisories."

async def test_msg91():
    print(f"Testing MSG91 Gateway for phone number: {phone_number}...")

    # Method 1: Send via MSG91 OTP / Verification Direct Route (No DLT template restriction for quick test)
    url_otp = f"https://control.msg91.com/api/v5/otp?template_id=&mobile={phone_number}&authkey={auth_key}&otp=9482"
    
    # Method 2: Standard Send SMS Route
    url_sms = "https://api.msg91.com/api/v2/sendsms"
    headers = {
        "authkey": auth_key,
        "content-type": "application/json"
    }
    payload = {
        "sender": "NERDIS",
        "route": "4",
        "country": "91",
        "sms": [
            {
                "message": message[:160],
                "to": [phone_number]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        print("\n--- Testing Route 1 (Standard SMS) ---")
        resp1 = await client.post(url_sms, headers=headers, json=payload)
        print("Status Code:", resp1.status_code)
        print("Response:", resp1.text)

        print("\n--- Testing Route 2 (Flow / OTP API) ---")
        resp2 = await client.get(f"https://control.msg91.com/api/v5/otp?mobile={phone_number}&authkey={auth_key}&otp=123456")
        print("Status Code:", resp2.status_code)
        print("Response:", resp2.text)

if __name__ == "__main__":
    asyncio.run(test_msg91())
