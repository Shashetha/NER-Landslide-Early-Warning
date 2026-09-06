from dotenv import load_dotenv
load_dotenv()

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from routes.prediction import router as prediction_router
from routes.alerts import router as alerts_router
from routes.reports import router as reports_router

app = FastAPI(
    title="Landslide Risk Monitoring API",
    description="AI-powered landslide risk prediction and early warning system for North East India",
    version=os.getenv("APP_VERSION", "1.0.0"),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://localhost:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    from database import init_pool, init_schema
    try:
        init_pool()
        init_schema()
        logger.info("Database ready")
    except Exception as exc:
        logger.error("Database initialisation failed: %s — running without DB", exc)


@app.get("/")
def root():
    return {
        "message": "Landslide Risk Monitoring API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "status": "healthy",
        "docs": "/api/docs",
    }


@app.get("/health")
def health_check():
    from datetime import datetime
    from services.prediction_service import prediction_service

    db_ok = False
    try:
        from database import get_db
        with get_db() as cur:
            cur.execute("SELECT 1")
        db_ok = True
    except Exception:
        pass

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": "connected" if db_ok else "unavailable",
        "ml_models": {
            "final_model": prediction_service._final_model is not None,
            "rainfall_model": prediction_service._rainfall_pkg is not None,
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true",
    )
