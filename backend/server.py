from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import random
import string
from datetime import datetime, timedelta

PORT = 8000

MOCK_ALERTS = [
    {
        "id": 1,
        "location": "Gangtok, Sikkim",
        "latitude": 27.3389,
        "longitude": 88.6065,
        "risk_level": "HIGH",
        "probability": 0.87,
        "status": "active",
        "affected_population": 2500,
        "description": "Heavy rainfall detected in the area with steep slope conditions.",
        "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(minutes=12)).isoformat() + "Z"
    },
    {
        "id": 2,
        "location": "Cherrapunji, Meghalaya",
        "latitude": 25.2630,
        "longitude": 91.7324,
        "risk_level": "CRITICAL",
        "probability": 0.94,
        "status": "active",
        "affected_population": 5200,
        "description": "Critical conditions detected. Multiple risk factors present in wettest place on Earth.",
        "created_at": (datetime.utcnow() - timedelta(hours=4)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(minutes=30)).isoformat() + "Z"
    },
    {
        "id": 3,
        "location": "Itanagar, Arunachal Pradesh",
        "latitude": 27.0844,
        "longitude": 93.6053,
        "risk_level": "HIGH",
        "probability": 0.79,
        "status": "active",
        "affected_population": 1800,
        "description": "Elevated soil moisture levels detected in hilly terrain.",
        "created_at": (datetime.utcnow() - timedelta(hours=6)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(minutes=45)).isoformat() + "Z"
    },
    {
        "id": 4,
        "location": "Shillong, Meghalaya",
        "latitude": 25.5788,
        "longitude": 91.8933,
        "risk_level": "MEDIUM",
        "probability": 0.62,
        "status": "resolved",
        "affected_population": 3100,
        "description": "Risk levels have decreased. Situation stabilized.",
        "created_at": (datetime.utcnow() - timedelta(hours=48)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(hours=12)).isoformat() + "Z"
    }
]

MOCK_REPORTS = []


class CleanAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ("/", "/health"):
            self._set_headers(200)
            res = {
                "message": "Landslide Risk Monitoring API is running",
                "version": "1.0.0",
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            self.wfile.write(json.dumps(res).encode('utf-8'))

        elif path == "/api/v1/alerts":
            self._set_headers(200)
            alerts = list(MOCK_ALERTS)
            if 'status' in query:
                alerts = [a for a in alerts if a['status'] == query['status'][0]]
            if 'risk_level' in query:
                alerts = [a for a in alerts if a['risk_level'] == query['risk_level'][0]]
            self.wfile.write(json.dumps(alerts).encode('utf-8'))

        elif path == "/api/v1/reports":
            self._set_headers(200)
            res = {"total": len(MOCK_REPORTS), "reports": MOCK_REPORTS}
            self.wfile.write(json.dumps(res).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"detail": "Not found"}).encode('utf-8'))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b'{}'
        
        try:
            body = json.loads(post_body.decode('utf-8'))
        except Exception:
            body = {}

        if path == "/api/v1/predictions":
            lat = float(body.get("latitude", 27.3389))
            lng = float(body.get("longitude", 88.6065))

            rainfall = round(random.uniform(50, 250), 2)
            slope = round(random.uniform(10, 50), 2)
            elevation = round(random.uniform(500, 2500), 2)
            soil_moisture = round(random.uniform(30, 80), 2)
            temperature = round(random.uniform(10, 25), 2)

            base_probability = random.uniform(0.3, 0.95)
            if rainfall > 150 and slope > 30:
                base_probability = min(base_probability + 0.15, 0.99)
            if soil_moisture > 70:
                base_probability = min(base_probability + 0.10, 0.99)

            probability = round(base_probability, 2)
            confidence = round(random.uniform(0.80, 0.95), 2)

            if probability >= 0.85:
                risk_level = "CRITICAL"
            elif probability >= 0.7:
                risk_level = "HIGH"
            elif probability >= 0.5:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            explanations = {
                "LOW": "Current environmental conditions indicate stable terrain with minimal landslide risk.",
                "MEDIUM": f"Moderate risk detected. Rainfall of {rainfall}mm with {slope}° slope requires close monitoring.",
                "HIGH": f"High rainfall ({rainfall}mm) combined with steep terrain ({slope}°) is increasing landslide probability.",
                "CRITICAL": f"CRITICAL RISK. Heavy rainfall ({rainfall}mm), steep slope ({slope}°), and saturated soil ({soil_moisture}%)."
            }

            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

            res = {
                "prediction_id": f"pred_{random_str}",
                "latitude": lat,
                "longitude": lng,
                "risk_level": risk_level,
                "probability": probability,
                "confidence": confidence,
                "features": {
                    "rainfall": rainfall,
                    "slope": slope,
                    "elevation": elevation,
                    "soil_moisture": soil_moisture,
                    "temperature": temperature
                },
                "explanation": explanations.get(risk_level, "Risk assessment completed."),
                "model_name": "landslide-model-mock",
                "model_version": "1.0.0",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode('utf-8'))

        elif path == "/api/v1/reports":
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            report_id = f"report_{random_str}"
            report_data = {
                "id": report_id,
                "location": body.get("location", ""),
                "latitude": body.get("latitude", 0.0),
                "longitude": body.get("longitude", 0.0),
                "hazard_type": body.get("hazard_type", "landslide"),
                "severity": body.get("severity", "medium"),
                "description": body.get("description", ""),
                "contact_info": body.get("contact_info", None),
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            MOCK_REPORTS.append(report_data)

            res = {
                "success": True,
                "report_id": report_id,
                "message": "Hazard report submitted successfully. Field team will investigate.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"detail": "Endpoint not found"}).encode('utf-8'))


if __name__ == "__main__":
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, CleanAPIHandler)
    print(f"Backend Server running at http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
