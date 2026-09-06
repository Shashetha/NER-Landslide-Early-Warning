"""
Pluggable Notification Gateway Architecture.
Supports TextBee Gateway (https://textbee.dev), SMTP Email, and Console Simulator.
"""

import os
import hashlib
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


# -------------------------------------------------------------
# 1. SMS PROVIDERS (TextBee Gateway)
# -------------------------------------------------------------
class SMSProvider(ABC):
    @abstractmethod
    async def send_sms(self, phone_number: str, message: str) -> Dict[str, Any]:
        pass


class TextBeeSMSProvider(SMSProvider):
    """
    TextBee SMS Gateway (https://textbee.dev).
    Sends real carrier SMS directly via connected Android device / TextBee API.
    """
    def __init__(self, api_key: str, device_id: str):
        self.api_key = api_key
        self.device_id = device_id

    async def send_sms(self, phone_number: str, message: str) -> Dict[str, Any]:
        clean_number = "".join(filter(lambda c: c.isdigit() or c == '+', phone_number.strip()))
        if not clean_number.startswith("+"):
            if len(clean_number) == 10:
                clean_number = f"+91{clean_number}"
            else:
                clean_number = f"+{clean_number}"

        url = f"https://api.textbee.dev/api/v1/gateway/devices/{self.device_id}/send-sms"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "recipients": [clean_number],
            "message": message
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                res_json = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"text": response.text}
                
                # Check response format: HTTP 200/201 and data.success == True
                is_ok = response.status_code in (200, 201, 202)
                data_obj = res_json.get("data", {}) if isinstance(res_json, dict) else {}
                success_flag = res_json.get("success") or data_obj.get("success") or ("smsBatchId" in str(res_json))

                if is_ok and success_flag:
                    batch_id = data_obj.get("smsBatchId") or res_json.get("smsBatchId") or "queued"
                    logger.info("[TEXTBEE SMS DELIVERED] To: %s | Batch ID: %s", clean_number, batch_id)
                    return {
                        "success": True,
                        "provider": "textbee",
                        "batch_id": batch_id,
                        "status": "DELIVERED"
                    }
                else:
                    logger.warning("[TEXTBEE SMS FAILED] %s: %s", clean_number, res_json)
                    return {"success": False, "provider": "textbee", "error": res_json}
        except Exception as e:
            logger.error("[TEXTBEE SMS EXCEPTION] %s", e)
            return {"success": False, "provider": "textbee", "error": str(e)}


class ConsoleSMSProvider(SMSProvider):
    async def send_sms(self, phone_number: str, message: str) -> Dict[str, Any]:
        logger.info("[SIMULATED SMS] To: %s | Message: %s", phone_number, message)
        return {"success": True, "provider": "console_sms", "status": "DELIVERED"}


# -------------------------------------------------------------
# 2. EMAIL PROVIDERS
# -------------------------------------------------------------
class EmailProvider(ABC):
    @abstractmethod
    async def send_email(self, recipient_email: str, subject: str, html_body: str) -> Dict[str, Any]:
        pass


class SMTPEmailProvider(EmailProvider):
    def __init__(self, host: str, port: int, user: str, password: str, from_email: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_email = from_email

    async def send_email(self, recipient_email: str, subject: str, html_body: str) -> Dict[str, Any]:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"NER Disaster Early Warning <{self.from_email}>"
            msg["To"] = recipient_email
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.from_email, recipient_email, msg.as_string())

            logger.info("[EMAIL SENT] To: %s | Subject: %s", recipient_email, subject)
            return {"success": True, "provider": "smtp_email", "status": "DELIVERED"}
        except Exception as e:
            logger.error("[EMAIL EXCEPTION] To %s: %s", recipient_email, e)
            return {"success": False, "provider": "smtp_email", "error": str(e)}


class ConsoleEmailProvider(EmailProvider):
    async def send_email(self, recipient_email: str, subject: str, html_body: str) -> Dict[str, Any]:
        logger.info("[SIMULATED EMAIL] To: %s | Subject: %s", recipient_email, subject)
        return {"success": True, "provider": "console_email", "status": "DELIVERED"}


# -------------------------------------------------------------
# FACTORY GETTERS
# -------------------------------------------------------------
def get_notification_gateways():
    from pathlib import Path
    from dotenv import load_dotenv
    _backend_dir = Path(__file__).resolve().parent.parent
    load_dotenv(_backend_dir / ".env", override=True)

    textbee_key = os.getenv("TEXTBEE_API_KEY")
    textbee_device = os.getenv("TEXTBEE_DEVICE_ID")

    if textbee_key and textbee_device and textbee_key.strip() and textbee_device.strip():
        logger.info("Using TextBee SMS Gateway (Device: %s)", textbee_device.strip()[:8])
        sms_gate = TextBeeSMSProvider(api_key=textbee_key.strip(), device_id=textbee_device.strip())
    else:
        sms_gate = ConsoleSMSProvider()

    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_from = os.getenv("SMTP_FROM", smtp_user or "alerts@ner-disaster.gov.in")
    email_gate = SMTPEmailProvider(smtp_host, smtp_port, smtp_user, smtp_pass, smtp_from) if (smtp_host and smtp_user and smtp_pass) else ConsoleEmailProvider()

    return sms_gate, email_gate


sms_provider, email_provider = get_notification_gateways()
