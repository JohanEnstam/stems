# 🚀 Utvecklingsstrategi för Stems

## 📋 Översikt

Denna strategi optimerar utvecklingsprocessen genom att separera lokal utveckling från molntestning, minimera onödiga deploys och säkerställa stabil produktion.

## 🌳 Branch-strategi

### Branches
- **`main`** → Production-ready kod, deploys automatiskt till **production** Cloud Run
- **`dev`** → Primär utvecklingsbranch, deploys automatiskt till **staging** Cloud Run  
- **`feature/*`** → Lokal utveckling, inga automatiska deploys

### Workflow
```
feature/upload → dev (staging deploy) → main (production deploy)
```

## 🔄 CI/CD Pipeline

### Automatiska Deploys
- **Push till `dev`** → Deploy till staging Cloud Run (`stems-web-staging`, `stems-worker-staging`)
- **Push till `main`** → Deploy till production Cloud Run (`stems-web`, `stems-worker`)

### Miljöer
- **Staging**: Billigare resurser (256Mi RAM, 1 CPU, max 3 instanser)
- **Production**: Fullständiga resurser (512Mi RAM, 1 CPU, max 10 instanser)

## 💻 Lokal vs Cloud Utveckling

### Lokal Utveckling (Snabb iteration)
```bash
# Aktivera environment
conda activate stems

# Starta services lokalt
make web      # http://localhost:8080
make worker   # http://localhost:8081

# Testa endpoints
curl http://localhost:8080/ping
curl http://localhost:8080/upload -F "file=@test.mp3"
```

**Fördelar:**
- ⚡ Snabb feedback (ingen väntan på deploys)
- 💰 Ingen kostnad
- 🔧 Enkel debugging
- 🧪 Perfekt för API-utveckling och enhetstester

### Cloud Testing (Integration)
```bash
# Push till dev för staging test
git checkout dev
git merge feature/upload
git push origin dev

# Testa staging URL (automatiskt deployad)
curl https://stems-web-staging-xxx.run.app/ping
```

**Fördelar:**
- ☁️ Testar verklig GCP-infrastruktur
- 🔗 Validerar bucket-integration
- 📊 Testar under belastning
- 🚀 Verifierar CI/CD-pipeline

## 🎯 Dummy MVP

### Syfte
Testa hela pipelinen utan att implementera komplett funktionalitet.

### Endpoints
- **`/`** → Frontend (HTML med drag-and-drop upload)
- **`/upload`** → Accepterar ljudfiler, returnerar jobb-ID
- **`/status/{job_id}`** → Simulerar olika jobb-statusar
- **`/ping`** → Health check för CI/CD

### Simulering
- **Upload**: Validerar filtyp men sparar inte
- **Processing**: Slumpmässiga statusar (processing/completed/failed)
- **Download**: Dummy-länkar för nedladdning

## 📝 Development Commands

### Lokal Utveckling
```bash
# Setup
conda activate stems
make install

# Development
make web          # Start web service
make worker       # Start worker service
make test         # Run tests

# Security
make security-check    # Pre-commit security audit
make security-setup    # Install pre-commit hooks
```

### Branch Management
```bash
# Skapa feature branch
git checkout -b feature/new-feature

# Merge till dev (staging deploy)
git checkout dev
git merge feature/new-feature
git push origin dev

# Merge till main (production deploy)
git checkout main
git merge dev
git push origin main
```

## 🔒 Säkerhet

### Pre-commit Hooks
- Automatisk säkerhetskontroll vid varje commit
- Förhindrar commits med säkerhetsproblem
- Körs lokalt innan push

### Environment Variables
- Alla känsliga värden via environment variables
- Olika konfigurationer för staging/production
- Inga hardcoded secrets i kod

## 📊 Monitoring

### Staging
- URL: `https://stems-web-staging-xxx.run.app`
- Resurser: Begränsade för kostnadseffektivitet
- Logs: Tillgängliga i GCP Console

### Production  
- URL: `https://stems-web-xxx.run.app`
- Resurser: Fullständiga för prestanda
- Monitoring: GCP Cloud Monitoring

## 🎯 Nästa Steg

1. **Testa Dummy MVP**: Push till `dev` och verifiera staging deploy
2. **Implementera Riktig Funktionalitet**: 
   - GCP bucket integration
   - Spotify API metadata
   - Demucs stem-splitting
3. **Frontend Förbättringar**: React/Next.js för bättre UX
4. **Monitoring**: Lägg till metrics och alerting

## 💡 Tips

- **Utveckla lokalt** för snabb iteration
- **Testa i staging** innan production deploy
- **Använd feature branches** för isolerad utveckling
- **Kör säkerhetskontroll** innan varje commit
- **Dokumentera ändringar** i commit messages
