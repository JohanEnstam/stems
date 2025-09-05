from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

app = FastAPI(
    title="Stems API",
    description="API för stem-splitting av musik",
    version="1.0.0"
)

# CORS middleware för frontend-integration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Säker: endast specificerade domäner
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Säker: endast nödvändiga metoder
    allow_headers=["Content-Type", "Authorization"],  # Säker: endast nödvändiga headers
)

@app.get("/")
async def root():
    """Root endpoint med grundläggande info"""
    return {
        "message": "Stems API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ping")
async def ping():
    """Health check endpoint för CI/CD pipeline"""
    return {
        "status": "ok",
        "message": "pong",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/health")
async def health():
    """Utökad health check med systeminfo"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0"
        # Inte exponera känslig systeminfo
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
