from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
import uuid

app = FastAPI(
    title="Stems API",
    description="API för stem-splitting av musik",
    version="1.0.0"
)

# Mount static files för frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    """Root endpoint - redirect till frontend"""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Dummy MVP: Upload endpoint som simulerar filhantering"""
    
    # Validera filtyp
    if not file.filename.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
        raise HTTPException(status_code=400, detail="Endast ljudfiler tillåtna")
    
    # Generera unikt jobb-ID
    job_id = str(uuid.uuid4())
    
    # Simulera filhantering (i riktig implementation skulle vi ladda till GCP bucket)
    file_size = 0
    if file.size:
        file_size = file.size
    
    return {
        "status": "uploaded",
        "job_id": job_id,
        "filename": file.filename,
        "file_size": file_size,
        "message": "Fil mottagen - dummy MVP",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Dummy MVP: Status endpoint för jobb"""
    
    # Simulera olika jobb-statusar
    import random
    statuses = ["processing", "completed", "failed"]
    status = random.choice(statuses)
    
    if status == "completed":
        return {
            "job_id": job_id,
            "status": status,
            "message": "Stem-splitting slutfört - dummy MVP",
            "download_links": {
                "vocals": f"https://dummy-download.com/{job_id}/vocals.wav",
                "drums": f"https://dummy-download.com/{job_id}/drums.wav",
                "bass": f"https://dummy-download.com/{job_id}/bass.wav",
                "other": f"https://dummy-download.com/{job_id}/other.wav"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    elif status == "failed":
        return {
            "job_id": job_id,
            "status": status,
            "message": "Stem-splitting misslyckades - dummy MVP",
            "error": "Simulerat fel för testning",
            "timestamp": datetime.utcnow().isoformat()
        }
    else:
        return {
            "job_id": job_id,
            "status": status,
            "message": "Bearbetar fil - dummy MVP",
            "progress": random.randint(10, 90),
            "timestamp": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
