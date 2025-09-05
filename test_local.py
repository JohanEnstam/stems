#!/usr/bin/env python3
"""
Enkel test-script för att verifiera lokal installation
"""

import sys
import subprocess
import requests
import time
from pathlib import Path

def test_web_service():
    """Testar web service lokalt"""
    print("🧪 Testing web service...")
    
    try:
        # Starta web service i bakgrunden
        web_dir = Path("web")
        if not web_dir.exists():
            print("❌ Web directory not found")
            return False
            
        # Installera dependencies
        print("📦 Installing web dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "web/requirements.txt"], 
                      check=True, capture_output=True)
        
        # Starta service
        print("🚀 Starting web service...")
        process = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", 
                                  "--host", "0.0.0.0", "--port", "8080"], 
                                 cwd="web", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Vänta på att service ska starta
        time.sleep(3)
        
        # Testa endpoints
        base_url = "http://localhost:8080"
        
        # Test /ping
        response = requests.get(f"{base_url}/ping", timeout=5)
        if response.status_code == 200:
            print("✅ /ping endpoint working")
        else:
            print(f"❌ /ping failed: {response.status_code}")
            return False
            
        # Test /health
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ /health endpoint working")
        else:
            print(f"❌ /health failed: {response.status_code}")
            return False
            
        # Test root
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root failed: {response.status_code}")
            return False
        
        # Stoppa process
        process.terminate()
        process.wait()
        
        print("✅ Web service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Web service test failed: {e}")
        return False

def test_worker_service():
    """Testar worker service lokalt"""
    print("🧪 Testing worker service...")
    
    try:
        worker_dir = Path("worker")
        if not worker_dir.exists():
            print("❌ Worker directory not found")
            return False
            
        # Installera dependencies
        print("📦 Installing worker dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "worker/requirements.txt"], 
                      check=True, capture_output=True)
        
        # Testa worker import
        sys.path.insert(0, "worker/src")
        from worker import StemWorker
        
        worker = StemWorker()
        status = worker.get_status()
        
        if status["status"] == "ready":
            print("✅ Worker service initialized successfully")
            return True
        else:
            print(f"❌ Worker status: {status}")
            return False
            
    except Exception as e:
        print(f"❌ Worker service test failed: {e}")
        return False

def main():
    """Huvudfunktion för tester"""
    print("🚀 Starting local tests for Stems project...")
    print("=" * 50)
    
    web_ok = test_web_service()
    print()
    worker_ok = test_worker_service()
    
    print("=" * 50)
    if web_ok and worker_ok:
        print("🎉 All tests passed! Ready for development.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
