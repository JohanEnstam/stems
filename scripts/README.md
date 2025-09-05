# 🔒 Säkerhetsverktyg för Stems Projekt

Denna mapp innehåller automatiserade säkerhetsverktyg för att säkerställa att projektet förblir säkert genom hela utvecklingsprocessen.

## 📁 Filer

### `security-check.sh`
Bash-baserad säkerhetskontroll som körs innan commits.

**Kontrollerar:**
- ✅ Känsliga filer (.env, *.json, *.key, etc.)
- ✅ .gitignore innehåll
- ✅ Python säkerhet (hårdkodade secrets, CORS)
- ✅ GitHub Actions säkerhet
- ✅ Docker säkerhet
- ✅ Python3 konsekvens
- ✅ Debug-information
- ✅ Miljövariabler
- ✅ Hårdkodade URLs med credentials
- ✅ Filbehörigheter

### `security_check.py`
Python-baserad säkerhetskontroll (alternativ till bash-scriptet).

**Samma kontroller som bash-scriptet men med Python.**

### `pre-commit-hook.sh`
Pre-commit hook som automatiskt kör säkerhetskontrollen innan varje commit.

## 🚀 Användning

### Manuell säkerhetskontroll
```bash
# Kör bash-versionen
./scripts/security-check.sh

# Eller kör Python-versionen
python3 scripts/security_check.py

# Eller via Makefile
make security-check
```

### Automatisk säkerhetskontroll (rekommenderat)
```bash
# Sätt upp pre-commit hook
make security-setup

# Nu körs säkerhetskontrollen automatiskt vid varje commit
git commit -m "Your commit message"
```

### Säkerhetskontroll i CI/CD
```bash
# Lägg till i GitHub Actions workflow
- name: Security Check
  run: ./scripts/security-check.sh
```

## 📊 Output

### ✅ Framgång
```
✅ SÄKERT att committa
```

### ⚠️ Varningar
```
⚠️ Säkerhetskontroller passerade med varningar
✅ SÄKERT att committa (men granska varningarna)
```

### ❌ Fel
```
❌ Säkerhetskontroller misslyckades
🚫 INTE säkert att committa - åtgärda felen först
```

## 🔧 Konfiguration

### Exkludera filer från kontroll
Redigera scripten för att exkludera specifika filer:

```bash
# I security-check.sh
if [[ "$file" == *"excluded_file.py" ]]; then
    continue
fi
```

### Lägg till nya säkerhetskontroller
Lägg till nya kontroller i båda scripten för konsistens.

## 🚨 Säkerhetsincidenter

Om säkerhetskontrollen misslyckas:

1. **Stoppa commit** omedelbart
2. **Granska felmeddelanden** noggrant
3. **Åtgärda problemen** enligt instruktioner
4. **Kör säkerhetskontrollen igen**
5. **Committa endast när allt är grönt**

## 📝 Best Practices

### Innan varje commit:
- [ ] Kör `make security-check`
- [ ] Granska alla varningar
- [ ] Åtgärda alla fel
- [ ] Verifiera att inga secrets exponeras

### Regelbundet:
- [ ] Uppdatera säkerhetskontroller
- [ ] Granska nya dependencies
- [ ] Kontrollera miljövariabler
- [ ] Verifiera .gitignore

## 🔄 Integration med utvecklingsflöde

### Pre-commit hooks (automatisk)
```bash
make security-setup  # Sätt upp en gång
# Sedan körs automatiskt vid varje commit
```

### Makefile integration
```bash
make security-check    # Kör säkerhetskontroll
make security-setup    # Sätt upp hooks
```

### CI/CD integration
Lägg till i GitHub Actions:
```yaml
- name: Security Check
  run: ./scripts/security-check.sh
```

---

**Kom ihåg:** Säkerhet är en process, inte en destination. Använd dessa verktyg konsekvent för att säkerställa att projektet förblir säkert! 🔒
