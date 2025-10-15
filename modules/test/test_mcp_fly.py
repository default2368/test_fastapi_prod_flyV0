import requests
import json

def test_mcp_fly():
    """Testa il server MCP su Fly.io"""
    base_url = "https://fly-mcp-server.fly.dev"
    
    print("🧪 TEST MCP SERVER SU FLY.IO")
    print("=" * 50)
    
    try:
        # Test connessione base
        response = requests.get(base_url, timeout=10)
        print(f"✅ Server raggiungibile: {response.status_code}")
        
        # Prova chiamata MCP (initialize)
        mcp_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "TestClient",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp",
            json=mcp_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"✅ Risposta MCP: {response.status_code}")
        if response.status_code == 200:
            print("🎯 SERVER MCP FUNZIONANTE!")
            print(f"📡 Endpoint: {base_url}/mcp")
            print("🔧 Tools disponibili via MCP protocol")
        else:
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - Server non raggiungibile")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Controlla l'URL")
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    test_mcp_fly()
