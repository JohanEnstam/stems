#!/bin/bash
# Setup script för Stems projekt

echo "🚀 Setting up Stems project..."

# Kontrollera att conda finns
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Anaconda or Miniconda first."
    exit 1
fi

# Aktivera stems-miljön
echo "📦 Activating conda environment 'stems'..."
conda activate stems

# Kontrollera Python version
echo "🐍 Python version:"
python3 --version

# Installera dependencies
echo "📦 Installing dependencies..."
cd web && python3 -m pip install -r requirements.txt
cd ../worker && python3 -m pip install -r requirements.txt
cd ..

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Make sure you're in the stems conda environment: conda activate stems"
echo "2. Test the setup: make test"
echo "3. Start web service: make web"
echo ""
echo "💡 Tip: Always run 'conda activate stems' before working on this project!"
