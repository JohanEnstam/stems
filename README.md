# Stems - Musik Stem-Splitting Service

Ett projekt för att separera musikstems (vocals, drums, bass, other) från MP3-filer med hjälp av AI/ML-tekniker.

## 🎯 MVP Funktioner

- Upload av MP3-filer till Google Cloud Storage
- Metadata-extraction från Spotify API (med fallback till lokal analys)
- Worker-service som kör stem-splitting (Demucs/Essentia/Aubio)
- Filer döpta med metadata
- Frontend för att övervaka processen och ladda ner resultat
- Ingen persistent lagring i MVP-fasen

## 🏗️ Arkitektur

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Frontend  │───▶│   Web API    │───▶│   Worker    │
│  (React)    │    │  (FastAPI)   │    │ (FastAPI)   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌──────────────┐    ┌─────────────┐
                    │ Cloud Storage│    │ Cloud Run   │
                    │   Bucket     │    │   Service   │
                    └──────────────┘    └─────────────┘
```

## 📂 Projektstruktur

```
stems/
├─ web/                    # Web API service
│  ├─ app/                 # FastAPI kod
│  │  └─ main.py          # Huvudapplikation
│  ├─ requirements.txt    # Python dependencies
│  └─ Dockerfile          # Container definition
│
├─ worker/                # Stem-splitting service
│  ├─ src/
│  │  └─ worker.py        # Worker implementation
│  ├─ requirements.txt    # Python dependencies
│  └─ Dockerfile          # Container definition
│
├─ infra/                 # Infrastructure definitions
│  ├─ terraform/          # Terraform configs (framtida)
│  └─ k8s/               # Kubernetes manifests (framtida)
│
├─ .github/
│  └─ workflows/
│     ├─ build-deploy-web.yml    # CI/CD för web service
│     └─ build-deploy-worker.yml # CI/CD för worker service
│
├─ scripts/                      # Säkerhetsverktyg
│  ├─ security-check.sh          # Bash säkerhetskontroll
│  ├─ security_check.py          # Python säkerhetskontroll
│  ├─ pre-commit-hook.sh         # Pre-commit hook
│  └─ README.md                  # Säkerhetsverktyg dokumentation
│
└─ README.md
```

## 🚀 Snabbstart

### Förutsättningar

- Python 3.11+
- Docker
- Google Cloud CLI (`gcloud`)
- GitHub CLI (`gh`)

### Lokal utveckling

1. **Klona repo och skapa virtuell miljö:**
   ```bash
   git clone <repo-url>
   cd stems
   
   # Skapa och aktivera conda-miljö
   conda create -n stems python=3.11 -y
   conda activate stems
   ```

2. **Installera dependencies:**
   ```bash
   # Använd setup-scriptet (rekommenderat)
   ./setup.sh
   
   # Eller manuellt:
   python3 -m pip install -r web/requirements.txt
   python3 -m pip install -r worker/requirements.txt
   ```

3. **Kör web service lokalt:**
   ```bash
   # Använd Makefile (rekommenderat)
   make web
   
   # Eller manuellt:
   cd web
   python3 -m uvicorn app.main:app --reload --port 8080
   ```

4. **Testa endpoints:**
   ```bash
   curl http://localhost:8080/ping
   curl http://localhost:8080/health
   ```

5. **Sätt upp säkerhetskontroll:**
   ```bash
   make security-setup  # Sätt upp pre-commit hooks
   make security-check  # Kör säkerhetskontroll manuellt
   ```

### Docker

```bash
# Bygg och kör web service
cd web
docker build -t stems-web .
docker run -p 8080:8080 stems-web

# Bygg och kör worker service
cd worker  
docker build -t stems-worker .
docker run -p 8081:8080 stems-worker
```

## ☁️ Google Cloud Setup

### Projekt och Bucket

```bash
# Sätt aktivt projekt
gcloud config set project stems-471207

# Verifiera bucket finns
gsutil ls gs://stems-input
```

### Artifact Registry

```bash
# Skapa registry (om den inte finns)
gcloud artifacts repositories create stems-repo \
  --repository-format=docker \
  --location=europe-north2
```

## 🔄 CI/CD Pipeline

### GitHub Actions Setup

1. **Skapa Service Account:**
   ```bash
   gcloud iam service-accounts create github-actions \
     --display-name="GitHub Actions"
   
   gcloud projects add-iam-policy-binding stems-471207 \
     --member="serviceAccount:github-actions@stems-471207.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding stems-471207 \
     --member="serviceAccount:github-actions@stems-471207.iam.gserviceaccount.com" \
     --role="roles/artifactregistry.writer"
   ```

2. **Skapa nyckel och lägg till i GitHub Secrets:**
   ```bash
   gcloud iam service-accounts keys create key.json \
     --iam-account=github-actions@stems-471207.iam.gserviceaccount.com
   ```
   
   Lägg till `key.json` innehållet som `GCP_SA_KEY` i GitHub repository secrets.

### Deployment

- **Automatisk deployment:** Push till `main` branch triggar deployment
- **Manual deployment:** Kör workflow från GitHub Actions tab

## 🧪 Testing

```bash
# Testa web service efter deployment
curl https://stems-web-xxxx.a.run.app/ping

# Förväntat svar:
{
  "status": "ok",
  "message": "pong", 
  "timestamp": "2024-01-XX...",
  "environment": "production"
}
```

## 🔒 Säkerhetsverktyg

Projektet inkluderar automatiserade säkerhetsverktyg:

- **`make security-check`** - Kör säkerhetskontroll manuellt
- **`make security-setup`** - Sätt upp automatiska pre-commit hooks
- **`./scripts/security-check.sh`** - Bash-baserad säkerhetskontroll
- **`python3 scripts/security_check.py`** - Python-baserad säkerhetskontroll

Se [scripts/README.md](scripts/README.md) för detaljerad dokumentation.

## 📋 Nästa Steg

- [ ] Implementera Spotify API integration
- [ ] Lägg till Demucs för stem-splitting
- [ ] Skapa frontend (React/Next.js)
- [ ] Implementera fil-upload funktionalitet
- [ ] Lägg till Pub/Sub för async processing
- [ ] Skapa Terraform för infrastructure as code

## 🐍 Virtuell Miljö

**VIKTIGT:** Detta projekt använder en dedikerad Conda-miljö för att undvika versionskonflikter.

### Aktivera miljön
```bash
conda activate stems
```

### Kontrollera att du är i rätt miljö
```bash
# Du ska se (stems) i din prompt
echo $CONDA_DEFAULT_ENV  # ska visa "stems"
python3 --version        # ska visa Python 3.11.x
```

### Om du får problem
- **Alias-konflikt:** Om `python` pekar på fel version, använd alltid `python3`
- **PATH-problem:** Kör `conda activate stems` innan varje session
- **Package-konflikter:** Ta bort och återskapa miljön: `conda remove -n stems --all && conda create -n stems python=3.11 -y`

## 🔧 Miljövariabler

### Web Service
- `ENVIRONMENT`: development/production
- `BUCKET_NAME`: Google Cloud Storage bucket namn
- `SPOTIFY_CLIENT_ID`: Spotify API client ID
- `SPOTIFY_CLIENT_SECRET`: Spotify API client secret

### Worker Service  
- `BUCKET_NAME`: Google Cloud Storage bucket namn
- `REGION`: GCP region (europe-north2)
- `MODEL_PATH`: Sökväg till Demucs modell

## 📝 Licens

MIT License - se LICENSE fil för detaljer.
