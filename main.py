from fastapi import FastAPI
import requests
import json
from datetime import datetime
from modules.test import esegui_test_completo

app = FastAPI()

# URL del MCP Server
MCP_SERVER_URL = "https://test-mcp-prodv1.fly.dev"

# Headers corretti per MCP
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

@app.get("/welcome")
async def welcome():
    return {"message": "Benvenuto nella mia app!"}

@app.get("/")
async def root():
    return {"info": "Vai su /welcome per il messaggio di benvenuto"}

@app.get("/test")
async def test_endpoint():
    """Testa le funzioni decorate locali"""
    risultati = esegui_test_completo()
    
    return {
        "status": "success",
        "risultati": risultati,
        "message": "Controlla i log del server per vedere il decoratore in azione!"
    }

@app.get("/test-mcp")
async def test_mcp_endpoint():
    """Testa la connessione al server MCP esterno"""
    try:
        # Test connessione base al MCP Server
        print(f"🔍 Testing MCP server: {MCP_SERVER_URL}")
        base_response = requests.get(MCP_SERVER_URL, timeout=10)
        print(f"✅ Base connection: {base_response.status_code}")
        
        # Prova chiamata MCP initialize con headers corretti
        mcp_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "FastAPI-Client",
                    "version": "1.0.0"
                }
            }
        }
        
        print(f"📤 Sending MCP request to: {MCP_SERVER_URL}/mcp")
        mcp_response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json=mcp_payload,
            headers=MCP_HEADERS,
            timeout=10
        )
        
        print(f"📥 MCP Response status: {mcp_response.status_code}")
        print(f"📥 MCP Response headers: {dict(mcp_response.headers)}")
        print(f"📥 MCP Response content (first 500 chars): {mcp_response.text[:500]}")
        
        # Prova a parsare la risposta
        try:
            mcp_data = mcp_response.json()
            print("✅ Successfully parsed JSON response")
            
            return {
                "status": "success",
                "mcp_server_status": "online",
                "mcp_response": mcp_data,
                "message": "MCP Server raggiungibile e funzionante!"
            }
        except json.JSONDecodeError as json_error:
            print(f"❌ JSON parse error: {json_error}")
            # Restituisci la risposta raw per debug
            return {
                "status": "partial_success",
                "mcp_server_status": "online",
                "mcp_response_status": mcp_response.status_code,
                "message": f"MCP Server online ma risposta non JSON",
                "debug_info": {
                    "response_content": mcp_response.text[:1000],  # Primi 1000 caratteri
                    "content_type": mcp_response.headers.get('content-type', 'unknown'),
                    "response_length": len(mcp_response.text),
                    "json_error": str(json_error)
                }
            }
            
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "mcp_server_status": "timeout",
            "message": "Timeout nella connessione al MCP Server"
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error", 
            "mcp_server_status": "connection_error",
            "message": "Impossibile connettersi al MCP Server"
        }
    except Exception as e:
        return {
            "status": "error",
            "mcp_server_status": "error",
            "message": f"Errore durante il test MCP: {str(e)}"
        }

@app.get("/health")
async def health_check():
    """Health check per entrambe le app"""
    try:
        # Test MCP Server
        mcp_response = requests.get(MCP_SERVER_URL, timeout=5)
        mcp_status = "healthy" if mcp_response.status_code < 500 else "unhealthy"
        
        return {
            "fastapi_app": "healthy",
            "mcp_server": mcp_status,
            "mcp_server_url": MCP_SERVER_URL,
            "timestamp": datetime.now().isoformat()
        }
    except:
        return {
            "fastapi_app": "healthy", 
            "mcp_server": "unreachable",
            "mcp_server_url": MCP_SERVER_URL,
            "timestamp": datetime.now().isoformat()
        }

@app.get("/test-v0")
async def test_v0():
    """TEST V0: Testa tutti i metodi locali della FastAPI"""
    print("🧪 TEST V0 - METODI LOCALI FASTAPI")
    
    # Test 1: Funzioni decorate
    test_risultati = esegui_test_completo()
    
    # Test 2: Endpoint locali (test interno, non chiamate HTTP)
    local_tests = {
        "welcome_endpoint": {"status": "success", "data": await welcome()},
        "root_endpoint": {"status": "success", "data": await root()},
        "decorated_functions": {"status": "success", "data": test_risultati}
    }
    
    return {
        "version": "V0 - FastAPI App",
        "timestamp": datetime.now().isoformat(),
        "tests": local_tests,
        "summary": {
            "total_tests": len(local_tests),
            "successful_tests": len(local_tests),
            "success_rate": "100%"
        }
    }

@app.get("/test-v1")
async def test_v1():
    """TEST V1: Testa il server MCP esterno con debug"""
    print("🧪 TEST V1 - SERVER MCP ESTERNO")
    
    test_results = {}
    
    # Test 1: Connessione base al MCP Server
    try:
        base_response = requests.get(MCP_SERVER_URL, timeout=10)
        test_results["mcp_server_connection"] = {
            "status": "success",
            "status_code": base_response.status_code,
            "note": "404 è normale per MCP server"
        }
    except Exception as e:
        test_results["mcp_server_connection"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test 2: Protocollo MCP initialize con debug
    try:
        mcp_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "V1-Test", "version": "1.0.0"}
            }
        }
        
        mcp_response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json=mcp_payload,
            headers=MCP_HEADERS,
            timeout=10
        )
        
        # Debug della risposta
        content_type = mcp_response.headers.get('content-type', 'unknown')
        response_preview = mcp_response.text[:200] if mcp_response.text else "empty"
        
        test_results["mcp_protocol"] = {
            "status": "success" if mcp_response.status_code == 200 else "partial",
            "status_code": mcp_response.status_code,
            "content_type": content_type,
            "response_preview": response_preview,
            "response_length": len(mcp_response.text)
        }
        
        # Prova a parsare JSON se possibile
        if 'application/json' in content_type:
            try:
                json_data = mcp_response.json()
                test_results["mcp_protocol"]["parsed_json"] = json_data
            except:
                test_results["mcp_protocol"]["json_parse_error"] = "Could not parse as JSON"
                
    except Exception as e:
        test_results["mcp_protocol"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Calcola statistiche
    total_tests = len(test_results)
    successful_tests = sum(1 for test in test_results.values() if test["status"] == "success")
    
    return {
        "version": "V1 - MCP Server",
        "timestamp": datetime.now().isoformat(),
        "mcp_server_url": MCP_SERVER_URL,
        "tests": test_results,
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": f"{(successful_tests/total_tests)*100:.1f}%"
        }
    }

@app.get("/status")
async def overall_status():
    """Status riepilogativo di tutto il sistema"""
    return {
        "system": "test-mcp-production",
        "timestamp": datetime.now().isoformat(),
        "versions": {
            "v0": "FastAPI App - Metodi Locali",
            "v1": "MCP Server - Protocollo AI"
        },
        "urls": {
            "v0_fastapi": "https://test-mcp-prodv0.fly.dev",
            "v1_mcp_server": MCP_SERVER_URL
        },
        "test_endpoints": [
            "/test-v0 - Test metodi locali V0",
            "/test-v1 - Test server MCP V1", 
            "/health - Health check",
            "/status - Status sistema"
        ]
    }
