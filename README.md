# Stems - Musik Stem-Splitting Service

Ett open-source projekt för att separera musikstems (vocals, drums, bass, other) från MP3-filer med hjälp av AI/ML-tekniker. Byggt med FastAPI, Google Cloud Platform och automatiserade säkerhetsverktyg.

## 🎯 MVP Funktioner

- Upload av MP3-filer till Google Cloud Storage
- Metadata-extraction från Spotify API (med fallback till lokal analys)
- Worker-service som kör stem-splitting (Demucs/Essentia/Aubio)
- Filer döpta med metadata
- Frontend för att övervaka processen och ladda ner resultat
- Ingen persistent lagring i MVP-fasen

## 🚀 Snabbstart

### Förutsättningar

- Python 3.11+
- Docker
- Google Cloud CLI (`gcloud`)
- GitHub CLI (`gh`)
- Spotify Developer Account (för API access)

### 1. Klona och sätt upp miljö

```bash
git clone https://github.com/JohanEnstam/stems.git
cd stems

# Skapa och aktivera conda-miljö
conda create -n stems python=3.11 -y
conda activate stems

# Installera dependencies
./setup.sh
```

### 2. Konfigurera Google Cloud

```bash
# Sätt aktivt projekt (ersätt med ditt projekt-ID)
gcloud config set project YOUR_PROJECT_ID

# Skapa bucket för filer
gsutil mb gs://YOUR_BUCKET_NAME

# Skapa Artifact Registry för Docker images
gcloud artifacts repositories create YOUR_REPO_NAME \
  --repository-format=docker \
  --location=YOUR_REGION
```

### 3. Konfigurera GitHub Secrets

Följ [GITHUB_SECRETS.md](GITHUB_SECRETS.md) för att sätta upp:
- `GCP_SA_KEY`
- `GCP_PROJECT_ID` 
- `GCP_REGION`
- `GCP_REGISTRY`
- `GCP_BUCKET_NAME`

### 4. Kör lokalt

```bash
# Starta web service
make web

# Testa endpoints
curl http://localhost:8080/ping
curl http://localhost:8080/health
```

### 5. Deploy till Cloud Run

```bash
# Push till main branch triggar automatisk deployment
git push origin main
```

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

## 🔧 Utveckling

### Lokal utveckling

```bash
# Aktivera miljö
conda activate stems

# Starta web service
make web

# Starta worker service  
make worker

# Kör säkerhetskontroll
make security-check
```

### Tillgängliga kommandon

```bash
make help           # Visa alla kommandon
make install        # Installera dependencies
make test           # Kör tester
make web            # Starta web service
make worker         # Starta worker service
make docker-build   # Bygg Docker images
make security-check # Kör säkerhetskontroll
make security-setup # Sätt upp pre-commit hooks
make clean          # Rensa temporära filer
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

## 🔄 CI/CD Pipeline

Projektet inkluderar automatiserad CI/CD med GitHub Actions:

- **Automatisk deployment** till Google Cloud Run
- **Docker image building** och push till Artifact Registry  
- **Säkerhetskontroller** i varje pipeline
- **Miljövariabler** via GitHub Secrets

Se [GITHUB_SECRETS.md](GITHUB_SECRETS.md) för detaljerad setup.

## 🧪 Testing

```bash
# Testa lokalt
make test

# Testa efter deployment
curl https://your-service-url.a.run.app/ping
```

## 🔒 Säkerhetsverktyg

Projektet inkluderar automatiserade säkerhetsverktyg:

- **`make security-check`** - Kör säkerhetskontroll manuellt
- **`make security-setup`** - Sätt upp automatiska pre-commit hooks
- **`./scripts/security-check.sh`** - Bash-baserad säkerhetskontroll
- **`python3 scripts/security_check.py`** - Python-baserad säkerhetskontroll

Se [scripts/README.md](scripts/README.md) för detaljerad dokumentation.

## 🤝 Bidra till Projektet

### Roadmap

- [ ] **Spotify API integration** - Metadata extraction från Spotify
- [ ] **Demucs integration** - AI-baserad stem-splitting
- [ ] **Frontend development** - React/Next.js interface
- [ ] **File upload** - Web interface för fil-upload
- [ ] **Pub/Sub integration** - Asynkron processing
- [ ] **Terraform infrastructure** - Infrastructure as Code

### Hur du bidrar

1. **Fork** repository
2. **Skapa feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (säkerhetskontroll körs automatiskt)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Öppna Pull Request**

### Development Guidelines

- **Säkerhet först:** Alla commits körs genom säkerhetskontroll
- **Python 3.11:** Använd `python3` konsekvent
- **Miljövariabler:** Använd `os.getenv()` för konfiguration
- **Dokumentation:** Uppdatera README för nya features
- **Testing:** Lägg till tester för nya funktionalitet

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
- `REGION`: GCP region (t.ex. europe-north2)
- `MODEL_PATH`: Sökväg till Demucs modell

## 📝 Licens

MIT License - se LICENSE fil för detaljer.
