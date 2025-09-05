#!/usr/bin/env python3
"""
🔒 Python-baserad säkerhetskontroll för Stems projekt
Körs som alternativ till bash-scriptet
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

class SecurityChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks = 0
        
    def log_error(self, message: str):
        print(f"❌ FEL: {message}")
        self.errors.append(message)
        
    def log_warning(self, message: str):
        print(f"⚠️  VARNING: {message}")
        self.warnings.append(message)
        
    def log_success(self, message: str):
        print(f"✅ {message}")
        
    def log_check(self, message: str):
        print(f"🔍 Kontrollerar: {message}")
        self.checks += 1
        
    def check_sensitive_files(self):
        """Kontrollera att inga känsliga filer finns"""
        self.log_check("Känsliga filer")
        
        sensitive_patterns = [
            "*.json", "*.key", "*.pem", "*.p12", ".env*", "*.log"
        ]
        
        sensitive_files = []
        for pattern in sensitive_patterns:
            if pattern.startswith("*"):
                # Hitta filer med extension
                ext = pattern[1:]
                for file_path in Path(".").rglob(f"*{ext}"):
                    if not any(ignore in str(file_path) for ignore in [".git", "node_modules", "__pycache__"]):
                        sensitive_files.append(str(file_path))
            else:
                # Hitta filer med namn
                for file_path in Path(".").rglob(pattern):
                    if not any(ignore in str(file_path) for ignore in [".git", "node_modules", "__pycache__"]):
                        sensitive_files.append(str(file_path))
        
        if sensitive_files:
            self.log_error("Känsliga filer hittades:")
            for file in sensitive_files:
                print(f"  - {file}")
            print("Lägg till dessa i .gitignore eller ta bort dem")
        else:
            self.log_success("Inga känsliga filer hittades")
            
    def check_gitignore(self):
        """Kontrollera .gitignore"""
        self.log_check(".gitignore innehåll")
        
        gitignore_path = Path(".gitignore")
        if not gitignore_path.exists():
            self.log_error(".gitignore saknas")
            return
            
        content = gitignore_path.read_text()
        required_patterns = ["*.json", ".env", "*.log"]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
                
        if missing_patterns:
            self.log_warning(f".gitignore saknar: {', '.join(missing_patterns)}")
        else:
            self.log_success(".gitignore innehåller nödvändiga exkluderingar")
            
    def check_python_security(self):
        """Kontrollera Python-filer för säkerhetsproblem"""
        self.log_check("Python säkerhet")
        
        python_files = list(Path(".").rglob("*.py"))
        
        for file_path in python_files:
            if any(ignore in str(file_path) for ignore in [".git", "node_modules", "__pycache__"]):
                continue
                
            try:
                content = file_path.read_text()
                
                # Kontrollera för hårdkodade secrets (exkludera vårt eget script)
                if "security_check.py" in str(file_path):
                    continue
                    
                secret_patterns = [
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    r'api_key\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']'
                ]
                
                for pattern in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.log_error(f"Hårdkodade secrets i {file_path}")
                        
                # Kontrollera för osäker CORS (exkludera vårt eget script)
                if "security_check.py" not in str(file_path) and 'allow_origins=["*"]' in content:
                    self.log_error(f"Osäker CORS konfiguration i {file_path}")
                    
                # Kontrollera att miljövariabler används
                if "os.getenv" in content:
                    self.log_success(f"Miljövariabler används korrekt i {file_path}")
                    
            except Exception as e:
                self.log_warning(f"Kunde inte läsa {file_path}: {e}")
                
    def check_github_actions(self):
        """Kontrollera GitHub Actions workflows"""
        self.log_check("GitHub Actions säkerhet")
        
        workflows_dir = Path(".github/workflows")
        if not workflows_dir.exists():
            self.log_warning("Inga GitHub Actions workflows hittades")
            return
            
        for workflow_file in workflows_dir.glob("*.yml"):
            try:
                content = workflow_file.read_text()
                
                # Kontrollera Python-användning
                if "python -m pip" in content or "python -m pytest" in content:
                    self.log_error(f"Osäker Python-användning i {workflow_file}")
                    
                # Kontrollera secrets
                if "secrets." in content:
                    self.log_success(f"Secrets används korrekt i {workflow_file}")
                    
            except Exception as e:
                self.log_warning(f"Kunde inte läsa {workflow_file}: {e}")
                
    def check_docker_security(self):
        """Kontrollera Docker-filer"""
        self.log_check("Docker säkerhet")
        
        dockerfiles = list(Path(".").rglob("Dockerfile"))
        
        for dockerfile in dockerfiles:
            if ".git" in str(dockerfile):
                continue
                
            try:
                content = dockerfile.read_text()
                
                if "USER app" in content:
                    self.log_success(f"Non-root user används i {dockerfile}")
                else:
                    self.log_warning(f"Ingen non-root user i {dockerfile}")
                    
                if "HEALTHCHECK" in content:
                    self.log_success(f"Health check konfigurerad i {dockerfile}")
                else:
                    self.log_warning(f"Ingen health check i {dockerfile}")
                    
            except Exception as e:
                self.log_warning(f"Kunde inte läsa {dockerfile}: {e}")
                
    def check_python3_consistency(self):
        """Kontrollera att python3 används konsekvent"""
        self.log_check("Python3 konsekvens")
        
        script_files = []
        for pattern in ["*.py", "*.sh", "Makefile"]:
            script_files.extend(Path(".").rglob(pattern))
            
        for script_file in script_files:
            if ".git" in str(script_file):
                continue
                
            try:
                content = script_file.read_text()
                
                # Kontrollera att python3 används istället för python
                if "python " in content and "python3" not in content:
                    self.log_warning(f"Använd python3 istället för python i {script_file}")
                    
            except Exception as e:
                self.log_warning(f"Kunde inte läsa {script_file}: {e}")
                
    def run_all_checks(self):
        """Kör alla säkerhetskontroller"""
        print("🔒 Säkerhets- och filcheck för Stems projekt")
        print("=" * 50)
        
        self.check_sensitive_files()
        self.check_gitignore()
        self.check_python_security()
        self.check_github_actions()
        self.check_docker_security()
        self.check_python3_consistency()
        
        # Sammanfattning
        print("\n" + "=" * 50)
        print("📊 SAMMANFATTNING:")
        print(f"Kontroller genomförda: {self.checks}")
        print(f"Varningar: {len(self.warnings)}")
        print(f"Fel: {len(self.errors)}")
        
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                print("🎉 Alla säkerhetskontroller passerade!")
                print("✅ SÄKERT att committa")
                return True
            else:
                print("⚠️  Säkerhetskontroller passerade med varningar")
                print("✅ SÄKERT att committa (men granska varningarna)")
                return True
        else:
            print("❌ Säkerhetskontroller misslyckades")
            print("🚫 INTE säkert att committa - åtgärda felen först")
            return False

def main():
    checker = SecurityChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
