import requests
import json

def test_all_endpoints():
    """Testa tutti gli endpoints della FastAPI su Fly.io"""
    
    # Sostituisci con il tuo URL reale di Fly.io
    BASE_URL = "https://az-mcp-server.fly.dev"  # ← MODIFICA QUESTA RIGA
    
    endpoints = [
        "/",
        "/welcome", 
        "/test",
        "/test-mcp",
        "/mcp-info"
    ]
    
    print("🧪 TEST ENDPOINTS FASTAPI SU FLY.IO")
    print("=" * 50)
    print(f"📡 Base URL: {BASE_URL}")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"\n🔍 Testing: {endpoint}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   📦 Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   📄 Response: {response.text}")
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"   💡 Message: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"❌ TIMEOUT: {endpoint}")
        except requests.exceptions.ConnectionError:
            print(f"❌ CONNECTION ERROR: {endpoint}")
        except Exception as e:
            print(f"❌ ERROR: {endpoint} - {e}")

def test_health():
    """Test di health check base"""
    BASE_URL = "https://az-mcp-server.fly.dev"  # ← MODIFICA QUESTA RIGA
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"\n🏥 HEALTH CHECK: {response.status_code}")
        return response.status_code == 200
    except:
        print("❌ HEALTH CHECK FAILED")
        return False

if __name__ == "__main__":
    if test_health():
        test_all_endpoints()
    else:
        print("❌ App non raggiungibile, controlla l'URL e lo stato su Fly.io")
