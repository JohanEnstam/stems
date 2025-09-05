#!/bin/bash
# 🔒 Säkerhets- och filcheck för Stems projekt
# Kör detta innan varje commit för att säkerställa säkerhet

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Räknare
ERRORS=0
WARNINGS=0
CHECKS=0

echo -e "${BLUE}🔒 Säkerhets- och filcheck för Stems projekt${NC}"
echo "=================================================="

# Funktion för att logga fel
log_error() {
    echo -e "${RED}❌ FEL: $1${NC}"
    ((ERRORS++))
}

# Funktion för att logga varningar
log_warning() {
    echo -e "${YELLOW}⚠️  VARNING: $1${NC}"
    ((WARNINGS++))
}

# Funktion för att logga framgång
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Funktion för att logga kontroll
log_check() {
    echo -e "${BLUE}🔍 Kontrollerar: $1${NC}"
    ((CHECKS++))
}

# 1. Kontrollera att inga känsliga filer finns
log_check "Känsliga filer"
SENSITIVE_FILES=$(find . -name "*.json" -o -name "*.key" -o -name "*.pem" -o -name "*.p12" -o -name ".env*" -o -name "*.log" 2>/dev/null | grep -v node_modules | grep -v ".git" || true)

if [ -n "$SENSITIVE_FILES" ]; then
    log_error "Känsliga filer hittades:"
    echo "$SENSITIVE_FILES"
    echo "Lägg till dessa i .gitignore eller ta bort dem"
else
    log_success "Inga känsliga filer hittades"
fi

# 2. Kontrollera .gitignore
log_check ".gitignore innehåll"
if [ -f ".gitignore" ]; then
    if grep -q "*.json" .gitignore && grep -q ".env" .gitignore && grep -q "*.log" .gitignore; then
        log_success ".gitignore innehåller nödvändiga exkluderingar"
    else
        log_warning ".gitignore saknar viktiga exkluderingar"
    fi
else
    log_error ".gitignore saknas"
fi

# 3. Kontrollera Python-filer för säkerhetsproblem
log_check "Python säkerhet"
PYTHON_FILES=$(find . -name "*.py" -not -path "./.git/*" -not -path "./node_modules/*")

for file in $PYTHON_FILES; do
    # Hoppa över vårt eget säkerhetsscript
    if [[ "$file" == *"security_check.py" ]]; then
        continue
    fi
    
    # Kontrollera för hårdkodade secrets
    if grep -qi "password.*=" "$file" || grep -qi "secret.*=" "$file" || grep -qi "api_key.*=" "$file"; then
        log_error "Hårdkodade secrets i $file"
    fi
    
    # Kontrollera för osäkra CORS inställningar
    if grep -q 'allow_origins=\["\*"\]' "$file"; then
        log_error "Osäker CORS konfiguration i $file (allow_origins=[\"*\"])"
    fi
    
    # Kontrollera att miljövariabler används
    if grep -q "os.getenv" "$file"; then
        log_success "Miljövariabler används korrekt i $file"
    fi
done

# 4. Kontrollera GitHub Actions workflows
log_check "GitHub Actions säkerhet"
if [ -d ".github/workflows" ]; then
    for workflow in .github/workflows/*.yml; do
        if [ -f "$workflow" ]; then
            # Kontrollera att python3 används istället för python
            if grep -q "python -m pip" "$workflow" || grep -q "python -m pytest" "$workflow"; then
                log_error "Osäker Python-användning i $workflow (använd python3)"
            fi
            
            # Kontrollera att secrets används korrekt
            if grep -q "secrets\." "$workflow"; then
                log_success "Secrets används korrekt i $workflow"
            fi
        fi
    done
else
    log_warning "Inga GitHub Actions workflows hittades"
fi

# 5. Kontrollera Docker-filer
log_check "Docker säkerhet"
DOCKERFILES=$(find . -name "Dockerfile" -not -path "./.git/*")

for dockerfile in $DOCKERFILES; do
    if grep -q "USER app" "$dockerfile"; then
        log_success "Non-root user används i $dockerfile"
    else
        log_warning "Ingen non-root user i $dockerfile"
    fi
    
    if grep -q "HEALTHCHECK" "$dockerfile"; then
        log_success "Health check konfigurerad i $dockerfile"
    else
        log_warning "Ingen health check i $dockerfile"
    fi
done

# 6. Kontrollera att alla Python-filer använder python3
log_check "Python3 konsekvens"
PYTHON_SCRIPTS=$(find . -name "*.py" -o -name "*.sh" -o -name "Makefile" 2>/dev/null | grep -v ".git" || true)

for script in $PYTHON_SCRIPTS; do
    if grep -q "python " "$script" && ! grep -q "python3" "$script"; then
        log_warning "Använd python3 istället för python i $script"
    fi
done

# 7. Kontrollera att inga debug-information exponeras
log_check "Debug-information"
if grep -r "print(" . --include="*.py" 2>/dev/null | grep -v "__pycache__" | grep -v ".git" > /dev/null 2>&1; then
    log_warning "Debug print-statements hittades i Python-filer"
fi

# 8. Kontrollera att miljövariabler är säkra
log_check "Miljövariabler"
if grep -r "os.getenv" . --include="*.py" 2>/dev/null | grep -v ".git" > /dev/null 2>&1; then
    log_success "Miljövariabler används korrekt"
else
    log_warning "Inga miljövariabler hittades - kontrollera att konfiguration är säker"
fi

# 9. Kontrollera att inga hårdkodade URLs med secrets
log_check "Hårdkodade URLs"
if grep -r "https://.*:.*@" . --include="*.py" --include="*.yml" --include="*.yaml" 2>/dev/null | grep -v ".git" > /dev/null 2>&1; then
    log_error "Hårdkodade URLs med credentials hittades"
fi

# 10. Kontrollera att alla filer har rätt behörigheter
log_check "Filbehörigheter"
if find . -name "*.sh" -not -perm 755 2>/dev/null | grep -v ".git" > /dev/null 2>&1; then
    log_warning "Några shell-script saknar körbehörigheter"
fi

# Sammanfattning
echo ""
echo "=================================================="
echo -e "${BLUE}📊 SAMMANFATTNING:${NC}"
echo -e "Kontroller genomförda: ${BLUE}$CHECKS${NC}"
echo -e "Varningar: ${YELLOW}$WARNINGS${NC}"
echo -e "Fel: ${RED}$ERRORS${NC}"

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 Alla säkerhetskontroller passerade!${NC}"
        echo -e "${GREEN}✅ SÄKERT att committa${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Säkerhetskontroller passerade med varningar${NC}"
        echo -e "${YELLOW}✅ SÄKERT att committa (men granska varningarna)${NC}"
        exit 0
    fi
else
    echo -e "${RED}❌ Säkerhetskontroller misslyckades${NC}"
    echo -e "${RED}🚫 INTE säkert att committa - åtgärda felen först${NC}"
    exit 1
fi
