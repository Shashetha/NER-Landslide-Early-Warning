# Landslide Risk Monitoring API

FastAPI backend for AI-powered landslide risk prediction and early warning system.

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Server

```bash
uvicorn main:app --reload
```

Or:

```bash
python main.py
```

Server will start at: `http://127.0.0.1:8000`

### 5. Test API

Open Swagger UI: `http://127.0.0.1:8000/api/docs`

## 📋 API Endpoints

### Predictions

- **POST** `/api/v1/predictions` - Predict landslide risk
  ```json
  {
    "latitude": 27.3389,
    "longitude": 88.6065
  }
  ```

- **GET** `/api/v1/predictions/model-info` - Get ML model information

### Alerts

- **GET** `/api/v1/alerts` - Get all alerts (supports filters)
- **GET** `/api/v1/alerts/{id}` - Get specific alert

### Reports

- **POST** `/api/v1/reports` - Submit hazard report
- **GET** `/api/v1/reports` - Get all reports

## 🏗️ Project Structure

```
backend/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── routes/                    # API route handlers
│   ├── prediction.py         # Prediction endpoints
│   ├── alerts.py             # Alert endpoints
│   └── reports.py            # Report endpoints
├── services/                  # Business logic
│   ├── prediction_service.py # Mock AI prediction
│   ├── alert_service.py      # Alert management
│   └── report_service.py     # Report handling
└── schemas/                   # Pydantic models
    ├── prediction.py         # Prediction schemas
    └── alert.py              # Alert/Report schemas
```

## 🔄 Integration Roadmap

### Phase 1: Mock API (Current) ✅
- FastAPI server running
- Mock predictions
- Mock alerts
- Mock reports

### Phase 2: Environmental Data
- Integrate rainfall API
- Integrate elevation API
- Integrate soil moisture sensors
- Integrate weather data

### Phase 3: Real ML Model
- Replace `MockPredictionService` with actual ML model
- Add model versioning
- Add prediction logging

### Phase 4: Database
- PostgreSQL/MySQL integration
- Store predictions
- Store alerts
- Store reports
- User authentication

## 🤖 ML Model Integration

### Requirements for Team A+B:

When ML model is ready, provide:

1. **Input Format:**
   ```python
   {
       "rainfall": float,      # mm
       "slope": float,         # degrees
       "elevation": float,     # meters
       "soil_moisture": float, # percentage
       "temperature": float    # celsius
   }
   ```

2. **Output Format:**
   ```python
   {
       "risk_level": str,      # LOW, MEDIUM, HIGH, CRITICAL
       "probability": float,   # 0-1
       "confidence": float     # 0-1
   }
   ```

3. **Model Files:**
   - Model weights (.h5, .pkl, .pt)
   - Preprocessing pipeline
   - Feature scaler
   - Model config

### Integration Steps:

1. Place model files in `backend/models/`
2. Update `prediction_service.py`:
   ```python
   # Replace mock prediction with:
   model = load_model("models/landslide_model.h5")
   prediction = model.predict(features)
   ```

## 🔗 Connect React Frontend

Update React `api.js`:

```javascript
const API_BASE_URL = "http://localhost:8000/api/v1";

export const api = {
  async getRiskPrediction(latitude, longitude) {
    const response = await fetch(`${API_BASE_URL}/predictions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latitude, longitude })
    });
    return await response.json();
  }
};
```

## 📊 Example API Usage

### Predict Risk

```bash
curl -X POST "http://localhost:8000/api/v1/predictions" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.3389, "longitude": 88.6065}'
```

Response:
```json
{
  "prediction_id": "pred_abc123",
  "latitude": 27.3389,
  "longitude": 88.6065,
  "risk_level": "HIGH",
  "probability": 0.84,
  "confidence": 0.91,
  "features": {
    "rainfall": 142,
    "slope": 32,
    "elevation": 1850,
    "soil_moisture": 72,
    "temperature": 19
  },
  "explanation": "High rainfall combined with steep terrain...",
  "model_name": "landslide-model-mock",
  "model_version": "1.0.0",
  "timestamp": "2026-09-04T14:15:00Z"
}
```

## 🛠️ Development

- Python 3.8+
- FastAPI 0.115+
- Uvicorn ASGI server
- Pydantic for data validation

## 📝 TODO

- [ ] Add authentication (JWT tokens)
- [ ] Add rate limiting
- [ ] Add request logging
- [ ] Connect to real database
- [ ] Integrate environmental APIs
- [ ] Replace mock ML with real model
- [ ] Add WebSocket for real-time alerts
- [ ] Add email/SMS notifications
- [ ] Deploy to cloud (AWS/GCP/Azure)
