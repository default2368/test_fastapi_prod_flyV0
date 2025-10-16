from fastapi import APIRouter
from modules.mcp_client.mcp_client import mcp_client

router = APIRouter(prefix="/mcp", tags=["MCP Server"])

@router.get("/test")
async def test_mcp_connection():
    """Testa la connessione al server MCP esterno"""
    try:
        result = await mcp_client.initialize_mcp()
        
        if result["status"] == "success":
            return {
                "status": "success",
                "mcp_server_status": "online",
                "protocol": result["protocol"],
                "initialize_result": result["initialize_result"],
                "all_events": result["all_events"],
                "message": "MCP Server funzionante con protocollo SSE!"
            }
        elif result["status"] == "partial_success":
            return {
                "status": "partial_success",
                "mcp_server_status": "online",
                "protocol": result["protocol"],
                "sse_events": result["sse_events"],
                "message": result.get("message", "MCP Server online ma risultato initialize non trovato")
            }
        else:
            return {
                "status": "error",
                "mcp_server_status": "error",
                "message": result.get("message", "Errore durante il test MCP")
            }
            
    except Exception as e:
        return {
            "status": "error",
            "mcp_server_status": "error",
            "message": f"Errore durante il test MCP: {str(e)}"
        }

@router.get("/tools")
async def list_mcp_tools():
    """Lista i tools disponibili sul server MCP"""
    result = await mcp_client.list_tools()
    
    if result["status"] == "success":
        return {
            "status": "success",
            "tools": result["tools_data"],
            "events": result["events"]
        }
    else:
        return {
            "status": "error",
            "message": result.get("message", "Errore nel recupero tools")
        }

@router.get("/full-test")
async def full_mcp_test():
    """Test completo del server MCP"""
    result = await mcp_client.full_test()
    
    # Calcola statistiche
    total_tests = len(result)
    successful_tests = sum(1 for test in result.values() if test["status"] == "success")
    
    return {
        "version": "MCP Server Test",
        "timestamp": "2025-10-15T10:00:00Z",  # Usa datetime in produzione
        "mcp_server_url": mcp_client.mcp_url,
        "tests": result,
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": f"{(successful_tests/total_tests)*100:.1f}%"
        }
    }

@router.get("/health")
async def mcp_health():
    """Health check del server MCP"""
    result = await mcp_client.test_connection()
    
    if result["status"] == "success":
        return {
            "mcp_server": "healthy",
            "status_code": result["status_code"],
            "note": result["note"]
        }
    else:
        return {
            "mcp_server": "unhealthy",
            "error": result["error"]
        }
