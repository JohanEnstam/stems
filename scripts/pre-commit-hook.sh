#!/bin/bash
# Pre-commit hook för Stems projekt
# Körs automatiskt innan varje commit

echo "🔒 Kör säkerhetskontroll innan commit..."

# Kör säkerhetskontrollen
./scripts/security-check.sh

# Om säkerhetskontrollen misslyckades, stoppa commit
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ COMMIT STOPPAD på grund av säkerhetsproblem"
    echo "Åtgärda felen och försök igen"
    exit 1
fi

echo ""
echo "✅ Säkerhetskontroll passerade - commit tillåten"
exit 0
