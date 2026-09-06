import os
import logging
from pathlib import Path
from dotenv import load_dotenv

_backend_dir = Path(__file__).resolve().parent
load_dotenv(_backend_dir / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from routes.auth import router as auth_router
from routes.prediction import router as prediction_router
from routes.alerts import router as alerts_router
from routes.reports import router as reports_router
from routes.gis import router as gis_router
from routes.notifications import router as notifications_router

app = FastAPI(
    title="NER Landslide Early Warning & Disaster Platform",
    description="Production-grade AI/ML Landslide Risk Prediction, GIS Heatmaps, and Disaster Management for North East India",
    version=os.getenv("APP_VERSION", "2.0.0"),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/api/docs", include_in_schema=False)
def api_docs_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


@app.get("/api/redoc", include_in_schema=False)
def api_redoc_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/redoc")


allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://localhost:3000,*",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = _backend_dir / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(prediction_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(gis_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    import database
    from services.alert_service import alert_service
    try:
        database.init_pool()
        database.init_schema()
        logger.info("Database and schema ready")

        # Automatically evaluate all 40 NER stations using real Open-Meteo telemetry on boot
        logger.info("Running initial live ML evaluation for all 40 NER stations...")
        await alert_service.sync_live_alerts_from_ml()
        logger.info("Live station telemetry synchronized to MySQL database")
    except Exception as exc:
        logger.error("Startup initialization notice: %s", exc)


@app.get("/")
def root():
    return {
        "title": "NER Landslide Early Warning & Disaster Platform",
        "version": os.getenv("APP_VERSION", "2.0.0"),
        "status": "online",
        "region": "North Eastern Region (NER), India",
        "states_covered": [
            "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya",
            "Mizoram", "Nagaland", "Sikkim", "Tripura"
        ],
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    from datetime import datetime
    import database
    from services.prediction_service import prediction_service

    db_ok = False
    if database._pool is not None:
        try:
            with database.get_db() as cur:
                cur.execute("SELECT 1")
                cur.fetchall()
                db_ok = True
        except Exception:
            pass

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": "connected" if db_ok else "unavailable",
        "ml_models": {
            "final_model": prediction_service._model is not None,
        },
    }


@app.get("/ready")
def readiness_check():
    return {"ready": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true",
    )
