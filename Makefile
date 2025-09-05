# Stems Project Makefile

.PHONY: help install test web worker docker-build docker-run clean

help: ## Visa denna hjälp
	@echo "Stems Project - Tillgängliga kommandon:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installera alla dependencies
	@echo "📦 Activating stems conda environment..."
	@conda activate stems || echo "⚠️  Please run: conda activate stems"
	@echo "📦 Installing web dependencies..."
	cd web && python3 -m pip install -r requirements.txt
	@echo "📦 Installing worker dependencies..."
	cd worker && python3 -m pip install -r requirements.txt

test: ## Kör lokala tester
	@echo "🧪 Running local tests..."
	@echo "⚠️  Make sure conda environment is activated: conda activate stems"
	python3 test_local.py

web: ## Starta web service lokalt
	@echo "🚀 Starting web service on http://localhost:8080"
	@echo "⚠️  Make sure conda environment is activated: conda activate stems"
	cd web && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

worker: ## Starta worker service lokalt
	@echo "🚀 Starting worker service on http://localhost:8081"
	@echo "⚠️  Make sure conda environment is activated: conda activate stems"
	cd worker && python3 -m uvicorn src.worker:create_worker_app --reload --host 0.0.0.0 --port 8081 --factory

docker-build: ## Bygg Docker images
	@echo "🐳 Building web service Docker image..."
	cd web && docker build -t stems-web .
	@echo "🐳 Building worker service Docker image..."
	cd worker && docker build -t stems-worker .

docker-run: ## Kör Docker containers
	@echo "🐳 Starting Docker containers..."
	docker run -d -p 8080:8080 --name stems-web stems-web
	docker run -d -p 8081:8080 --name stems-worker stems-worker
	@echo "✅ Services running:"
	@echo "   Web: http://localhost:8080"
	@echo "   Worker: http://localhost:8081"

docker-stop: ## Stoppa Docker containers
	@echo "🛑 Stopping Docker containers..."
	docker stop stems-web stems-worker || true
	docker rm stems-web stems-worker || true

clean: ## Rensa temporära filer
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

security-check: ## Kör säkerhetskontroll
	@echo "🔒 Running security check..."
	./scripts/security-check.sh

security-setup: ## Sätt upp säkerhetshooks
	@echo "🔧 Setting up security hooks..."
	@if [ -d ".git" ]; then \
		cp scripts/pre-commit-hook.sh .git/hooks/pre-commit; \
		chmod +x .git/hooks/pre-commit; \
		echo "✅ Pre-commit hook installed"; \
	else \
		echo "⚠️  Not a git repository - run 'git init' first"; \
	fi

deploy-check: ## Kontrollera att allt är redo för deployment
	@echo "🔍 Checking deployment readiness..."
	@echo "✅ Project structure:"
	@ls -la web/app/main.py worker/src/worker.py .github/workflows/ || echo "❌ Missing files"
	@echo "✅ Dockerfiles:"
	@ls -la web/Dockerfile worker/Dockerfile || echo "❌ Missing Dockerfiles"
	@echo "✅ GitHub Actions:"
	@ls -la .github/workflows/*.yml || echo "❌ Missing workflows"
	@echo ""
	@echo "📋 Next steps:"
	@echo "1. Create GitHub repository"
	@echo "2. Set up GCP service account"
	@echo "3. Add GCP_SA_KEY to GitHub secrets"
	@echo "4. Push to main branch to trigger deployment"
