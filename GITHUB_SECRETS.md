# 🔐 GitHub Secrets Setup Guide

Denna guide visar hur du konfigurerar GitHub Secrets för säker CI/CD deployment.

## 📋 Required Secrets

För att CI/CD ska fungera behöver du lägga till följande secrets i ditt GitHub repository:

### 🔑 Secrets som måste läggas till:

| Secret Name | Beskrivning | Exempel |
|-------------|-------------|---------|
| `GCP_SA_KEY` | Service Account JSON key | `{"type": "service_account", ...}` |
| `GCP_PROJECT_ID` | Ditt GCP projekt-ID | `your-project-123456` |
| `GCP_REGION` | GCP region | `europe-north2` |
| `GCP_REGISTRY` | Artifact Registry URL | `europe-north2-docker.pkg.dev` |
| `GCP_BUCKET_NAME` | Cloud Storage bucket | `your-bucket-name` |

## 🚀 Setup Instructions

### 1. Skapa Service Account
```bash
# Ersätt YOUR_PROJECT_ID med ditt faktiska projekt-ID
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

### 2. Skapa Service Account Key
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 3. Lägg till Secrets i GitHub

1. Gå till ditt GitHub repository
2. Klicka på **Settings** → **Secrets and variables** → **Actions**
3. Klicka på **New repository secret**
4. Lägg till varje secret enligt tabellen ovan

#### GCP_SA_KEY
- **Namn:** `GCP_SA_KEY`
- **Värde:** Kopiera hela innehållet från `key.json` filen

#### GCP_PROJECT_ID
- **Namn:** `GCP_PROJECT_ID`
- **Värde:** Ditt GCP projekt-ID (t.ex. `your-project-123456`)

#### GCP_REGION
- **Namn:** `GCP_REGION`
- **Värde:** Din GCP region (t.ex. `europe-north2`)

#### GCP_REGISTRY
- **Namn:** `GCP_REGISTRY`
- **Värde:** Din Artifact Registry URL (t.ex. `europe-north2-docker.pkg.dev`)

#### GCP_BUCKET_NAME
- **Namn:** `GCP_BUCKET_NAME`
- **Värde:** Ditt Cloud Storage bucket namn (t.ex. `your-bucket-name`)

## 🔒 Säkerhet

### ✅ Säkerhetsåtgärder:
- **Inga hårdkodade värden** i koden
- **Alla känsliga data** via GitHub Secrets
- **Service Account** med minimala behörigheter
- **Automatisk säkerhetskontroll** vid varje commit

### 🚨 Viktiga säkerhetsnoter:
- **Ta bort `key.json`** efter att du lagt till den i GitHub Secrets
- **Lägg aldrig till `key.json`** i git repository
- **Använd endast nödvändiga behörigheter** för Service Account
- **Rotera nycklar regelbundet** för säkerhet

## 🧪 Testa Setup

Efter att du lagt till alla secrets:

1. **Push en ändring** till main branch
2. **Gå till GitHub Actions** tab i ditt repository
3. **Kontrollera att workflow körs** utan fel
4. **Verifiera deployment** till Cloud Run

## 🔧 Troubleshooting

### Vanliga problem:

#### "Permission denied"
- Kontrollera att Service Account har rätt behörigheter
- Verifiera att `GCP_SA_KEY` är korrekt formaterad JSON

#### "Project not found"
- Kontrollera att `GCP_PROJECT_ID` är korrekt
- Verifiera att projektet finns och är aktivt

#### "Bucket not found"
- Kontrollera att `GCP_BUCKET_NAME` är korrekt
- Verifiera att bucket finns i rätt region

#### "Registry not found"
- Kontrollera att `GCP_REGISTRY` är korrekt
- Verifiera att Artifact Registry finns

---

**Kom ihåg:** Alla känsliga värden ska nu komma från GitHub Secrets, inte från hårdkodade värden i koden! 🔐
