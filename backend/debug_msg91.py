import os
import sys
import asyncio
import httpx

auth_key = "568268AYnishnksQ76a9d47c4P1"
phone_number = "918778339906"

async def check_msg91_balance_and_otp():
    print("1. Checking MSG91 Account Balance & Routes...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Check balance
        bal_res = await client.get(f"https://control.msg91.com/api/v5/widget/getBalance?authkey={auth_key}")
        print("Balance API Response:", bal_res.text)

        # Send via MSG91 OTP route (OTP route bypasses promotional DLT filters on Indian carriers like Jio/Airtel/Vi)
        print("\n2. Sending via MSG91 Direct OTP Channel to +918778339906...")
        otp_url = f"https://control.msg91.com/api/v5/otp?mobile={phone_number}&authkey={auth_key}&otp=9482&template_id=&otp_length=4&otp_expiry=10"
        otp_res = await client.get(otp_url)
        print("OTP Route Response:", otp_res.status_code, otp_res.text)

if __name__ == "__main__":
    asyncio.run(check_msg91_balance_and_otp())
