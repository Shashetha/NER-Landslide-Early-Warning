import os
import sys
import asyncio
import httpx

auth_key = "568268AYnishnksQ76a9d47c4P1"

async def check_msg91_reports():
    print("Fetching real-time SMS delivery report from MSG91 server...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Request ID from previous send: 3669667055636a7a72747965
        url = f"https://api.msg91.com/api/v5/otp/verify?mobile=918778339906&authkey={auth_key}&otp=9482"
        # Check logs
        log_url = f"https://control.msg91.com/api/v5/report/sms?authkey={auth_key}"
        res = await client.get(log_url)
        print("MSG91 Reports Response:", res.status_code, res.text[:300])

if __name__ == "__main__":
    asyncio.run(check_msg91_reports())
