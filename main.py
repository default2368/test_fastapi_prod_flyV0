from fastapi import FastAPI
import requests
import json
from datetime import datetime
from modules.test import esegui_test_completo

app = FastAPI()

# URL del MCP Server
MCP_SERVER_URL = "https://test-mcp-prodv1.fly.dev"

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
        response = requests.get(MCP_SERVER_URL, timeout=10)
        
        # Prova chiamata MCP initialize
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
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if mcp_response.status_code == 200:
            mcp_data = mcp_response.json()
            return {
                "status": "success",
                "mcp_server_status": "online",
                "mcp_response": mcp_data,
                "message": "MCP Server raggiungibile e funzionante!"
            }
        else:
            return {
                "status": "partial_success",
                "mcp_server_status": "online",
                "mcp_response_status": mcp_response.status_code,
                "message": f"MCP Server online ma errore protocollo: {mcp_response.text}"
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

@app.get("/mcp-tools")
async def list_mcp_tools():
    """Lista i tools disponibili sul server MCP"""
    return {
        "mcp_server": MCP_SERVER_URL,
        "available_tools": [
            "get_server_info",
            "calculate_operation", 
            "format_text",
            "get_system_status"
        ],
        "note": "I tools sono disponibili via protocollo MCP sul server esterno"
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

@app.get("/test-production")
async def test_production_complete():
    """Test completo di tutto il setup di produzione"""
    test_results = {}
    
    # Test 1: Health Check
    try:
        health_response = requests.get(f"https://test-mcp-prodv0.fly.dev/health", timeout=10)
        test_results["health_check"] = {
            "status": "success" if health_response.status_code == 200 else "failed",
            "status_code": health_response.status_code,
            "data": health_response.json() if health_response.status_code == 200 else health_response.text
        }
    except Exception as e:
        test_results["health_check"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test 2: Endpoints Locali
    try:
        welcome_response = requests.get(f"https://test-mcp-prodv0.fly.dev/welcome", timeout=10)
        test_results["welcome_endpoint"] = {
            "status": "success" if welcome_response.status_code == 200 else "failed",
            "status_code": welcome_response.status_code,
            "data": welcome_response.json() if welcome_response.status_code == 200 else welcome_response.text
        }
    except Exception as e:
        test_results["welcome_endpoint"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test 3: Test Endpoint
    try:
        test_response = requests.get(f"https://test-mcp-prodv0.fly.dev/test", timeout=10)
        test_results["test_endpoint"] = {
            "status": "success" if test_response.status_code == 200 else "failed",
            "status_code": test_response.status_code,
            "data": test_response.json() if test_response.status_code == 200 else test_response.text
        }
    except Exception as e:
        test_results["test_endpoint"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test 4: MCP Server Connection
    try:
        mcp_response = requests.get(f"https://test-mcp-prodv0.fly.dev/test-mcp", timeout=10)
        test_results["mcp_connection"] = {
            "status": "success" if mcp_response.status_code == 200 else "failed",
            "status_code": mcp_response.status_code,
            "data": mcp_response.json() if mcp_response.status_code == 200 else mcp_response.text
        }
    except Exception as e:
        test_results["mcp_connection"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test 5: MCP Server Direct
    try:
        direct_mcp_response = requests.get(MCP_SERVER_URL, timeout=10)
        test_results["mcp_server_direct"] = {
            "status": "success" if direct_mcp_response.status_code < 500 else "failed",
            "status_code": direct_mcp_response.status_code,
            "note": "MCP server risponde (404 è normale per MCP)"
        }
    except Exception as e:
        test_results["mcp_server_direct"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Calcola riepilogo
    total_tests = len(test_results)
    successful_tests = sum(1 for test in test_results.values() if test["status"] == "success")
    
    return {
        "test_summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": f"{(successful_tests/total_tests)*100:.1f}%",
            "timestamp": datetime.now().isoformat()
        },
        "detailed_results": test_results,
        "urls_tested": {
            "fastapi_app": "https://test-mcp-prodv0.fly.dev",
            "mcp_server": MCP_SERVER_URL
        }
    }

@app.get("/status")
async def overall_status():
    """Status riepilogativo di tutto il sistema"""
    try:
        # Test FastAPI app
        health = await health_check()
        
        # Test MCP connection
        mcp_test = await test_mcp_endpoint()
        
        return {
            "system": "test-mcp-production",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "fastapi_app": health["fastapi_app"],
                "mcp_server": health["mcp_server"],
                "mcp_connection": mcp_test["status"]
            },
            "urls": {
                "fastapi": "https://test-mcp-prodv0.fly.dev",
                "mcp_server": MCP_SERVER_URL
            },
            "endpoints_available": [
                "/", "/welcome", "/test", "/test-mcp", "/mcp-tools", 
                "/health", "/test-production", "/status"
            ]
        }
    except Exception as e:
        return {
            "system": "test-mcp-production",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
