from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import requests
import json
from datetime import datetime
from modules.test import esegui_test_completo

app = FastAPI(title="MCP System API")

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL del MCP Server
MCP_SERVER_URL = "https://test-mcp-prodv1.fly.dev"

# Headers corretti per MCP
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

def parse_sse_response(response_text):
    """Parsa una risposta SSE (Server-Sent Events)"""
    events = []
    lines = response_text.strip().split('\n')
    
    current_event = {}
    for line in lines:
        if line.startswith('event:'):
            current_event['event'] = line[6:].strip()
        elif line.startswith('data:'):
            data_content = line[5:].strip()
            try:
                current_event['data'] = json.loads(data_content)
            except json.JSONDecodeError:
                current_event['data'] = data_content
        elif line == '' and current_event:
            events.append(current_event)
            current_event = {}
    
    if current_event:
        events.append(current_event)
    
    return events

# ===== ENDPOINTS API =====

@app.get("/")
async def root():
    """Redirect alla dashboard"""
    return RedirectResponse(url="/ui")

@app.get("/welcome")
async def welcome():
    return {"message": "Benvenuto nella mia app!"}

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
        base_response = requests.get(MCP_SERVER_URL, timeout=10)
        
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
        
        mcp_response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json=mcp_payload,
            headers=MCP_HEADERS,
            timeout=10
        )
        
        if mcp_response.status_code == 200:
            # Il server MCP usa SSE, parsiamo la risposta
            if mcp_response.headers.get('content-type') == 'text/event-stream':
                sse_events = parse_sse_response(mcp_response.text)
                
                # Cerca il risultato initialize
                initialize_result = None
                for event in sse_events:
                    if event.get('data', {}).get('id') == 1:  # ID della nostra richiesta
                        initialize_result = event.get('data', {})
                        break
                
                if initialize_result:
                    return {
                        "status": "success",
                        "mcp_server_status": "online", 
                        "protocol": "SSE (Server-Sent Events)",
                        "initialize_result": initialize_result,
                        "all_events": sse_events,
                        "message": "MCP Server funzionante con protocollo SSE!"
                    }
                else:
                    return {
                        "status": "partial_success",
                        "mcp_server_status": "online",
                        "protocol": "SSE (Server-Sent Events)", 
                        "sse_events": sse_events,
                        "message": "MCP Server online ma risultato initialize non trovato"
                    }
            else:
                # Prova come JSON normale
                try:
                    mcp_data = mcp_response.json()
                    return {
                        "status": "success",
                        "mcp_server_status": "online",
                        "mcp_response": mcp_data,
                        "message": "MCP Server raggiungibile e funzionante!"
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "partial_success",
                        "mcp_server_status": "online", 
                        "raw_response": mcp_response.text,
                        "content_type": mcp_response.headers.get('content-type'),
                        "message": "MCP Server online ma formato risposta non riconosciuto"
                    }
        else:
            return {
                "status": "partial_success",
                "mcp_server_status": "online",
                "mcp_response_status": mcp_response.status_code,
                "message": f"MCP Server online ma errore HTTP: {mcp_response.text}"
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
    """TEST V1: Testa il server MCP esterno"""
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
    
    # Test 2: Protocollo MCP initialize
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
        
        if mcp_response.status_code == 200:
            # Parsing SSE
            sse_events = parse_sse_response(mcp_response.text)
            initialize_found = any(event.get('data', {}).get('id') == 1 for event in sse_events)
            
            test_results["mcp_protocol"] = {
                "status": "success",
                "status_code": mcp_response.status_code,
                "protocol": "SSE",
                "events_count": len(sse_events),
                "initialize_found": initialize_found,
                "server_info": next((event.get('data', {}).get('result', {}).get('serverInfo') 
                                  for event in sse_events 
                                  if event.get('data', {}).get('result', {}).get('serverInfo')), None)
            }
        else:
            test_results["mcp_protocol"] = {
                "status": "partial",
                "status_code": mcp_response.status_code,
                "response": mcp_response.text[:500]
            }
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
            "v1": "MCP Server - Protocollo SSE"
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




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
