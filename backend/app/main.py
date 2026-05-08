import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import auth, dashboard, exports, uploads
from app.api.analytics import router as analytics_router
from app.core.database import _get_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection verified successfully.")
    except RuntimeError as exc:
        # DATABASE_URL not configured — log clearly and abort startup.
        logger.critical("Startup failed: %s", exc)
        raise
    except Exception as exc:
        # DATABASE_URL is set but the database is unreachable.
        logger.critical("Startup failed: could not connect to the database: %s", exc)
        raise

    yield
    # --- shutdown (nothing to do) ---


app = FastAPI(
    title="X-CAT Supply Chain Analysis Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(uploads.router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(exports.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "x-cat"}
