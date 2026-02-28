from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
  
from core.config import settings
from core.logging import setup_logging
from voice.session_manager import session_manager
from voice.flow_manager import flow_manager
from api.routes import kb, admin, auth, organisations, call_flow, products, call_flow_v2
from api.routes import superadmin_platform, admin_organisations, admin_companies, organisation_companies  # Multi-tenant routes
from api.routes import pending_approvals  # Pending approvals for super admin
from api.routes import organisation_pending_approvals  # Pending approvals for organisations
from api.routes import company_profile  # Company profile
from api.routes import company_brands  # Company brand management
from api.routes.organisations import brand_router, product_router
# from api.routes import exotel_passthru  # Production-ready Exotel Passthru webhook
# from api.routes import exotel_calling  # NEW: Exotel Live Calling System

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kisan Vani AI Backend with MySQL")
    await session_manager.connect()
    await flow_manager.initialize()
    logger.info("Services initialized")
    yield
    logger.info("Shutting down")
    await session_manager.disconnect()

app = FastAPI(
    title="Kisan Vani AI",
    description="AI Voice Advisory Platform for Indian Farmers",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Allow all origins including file://
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)



# Include all routes
app.include_router(auth.router, prefix="/api")
app.include_router(kb.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(call_flow.router, prefix="/api/call-flow", tags=["Call Flow"])
app.include_router(call_flow_v2.router, prefix="/api/call-flow", tags=["Call Flow V2"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(superadmin_platform.router, prefix="/api/superadmin", tags=["Super Admin Platform"])
app.include_router(pending_approvals.router, prefix="/api/superadmin", tags=["Pending Approvals"])
app.include_router(organisation_pending_approvals.router, prefix="/api/organisation", tags=["Organisation Pending Approvals"])
app.include_router(admin_organisations.router, prefix="/api/admin", tags=["Admin - Organisations"])  # Admin role organisations
app.include_router(admin_companies.router, prefix="/api/admin", tags=["Admin - Companies"])  # Admin role companies
app.include_router(organisations.router, prefix="/api")
app.include_router(organisation_companies.router, prefix="/api", tags=["Organisation - Companies"])  # Multi-tenant
app.include_router(brand_router, prefix="/api")
app.include_router(product_router, prefix="/api")
app.include_router(company_profile.router, prefix="/api/company", tags=["Company Profile"])
app.include_router(company_brands.router, prefix="/api/company", tags=["Company Brands"])

# ============================================================================
# STATIC FILES FOR AUDIO SERVING (REQUIRED FOR EXOTEL <Play> TAG)
# ============================================================================
# Exotel's <Play> tag needs publicly accessible audio URLs
# We save TTS-generated audio and serve it via /static/audio/
# In production, use S3/GCS instead of local filesystem

audio_dir = Path("/app/static/audio")
audio_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="/app/static"), name="static")

@app.get("/api/")
async def root():
    return {
        "message": "Kisan Vani AI - Voice Advisory Platform",
        "version": "1.0.0",
        "status": "active",
        "database": "MySQL (Production)"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "MySQL 10.11",
            "redis": "connected",
            "qdrant": "configured"
        }
    }

logger.info("✅ Kisan Vani AI Production Server with MySQL Started")
logger.info("🚀 Access API docs at: http://localhost:8001/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8001,
        
    )
