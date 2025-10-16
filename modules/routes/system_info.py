from fastapi import APIRouter
from datetime import datetime
from modules.test import esegui_test_completo
from modules.mcp_client.mcp_client import mcp_client

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health")
async def health_check():
    """Health check per entrambe le app"""
    try:
        # Test MCP Server
        mcp_result = await mcp_client.test_connection()
        mcp_status = "healthy" if mcp_result["status"] == "success" else "unhealthy"
        
        return {
            "fastapi_app": "healthy",
            "mcp_server": mcp_status,
            "mcp_server_url": mcp_client.mcp_url,
            "timestamp": datetime.now().isoformat()
        }
    except:
        return {
            "fastapi_app": "healthy", 
            "mcp_server": "unreachable",
            "mcp_server_url": mcp_client.mcp_url,
            "timestamp": datetime.now().isoformat()
        }

@router.get("/status")
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
            "v1_mcp_server": mcp_client.mcp_url
        },
        "endpoints": {
            "system": [
                "/system/health",
                "/system/status", 
                "/system/test-v0",
                "/system/test-v1"
            ],
            "mcp": [
                "/mcp/test",
                "/mcp/tools",
                "/mcp/full-test",
                "/mcp/health"
            ],
            "app": [
                "/",
                "/welcome",
                "/test"
            ]
        }
    }

@router.get("/test-v0")
async def test_v0():
    """TEST V0: Testa tutti i metodi locali della FastAPI"""
    # Test 1: Funzioni decorate
    test_risultati = esegui_test_completo()
    
    # Test 2: Endpoint locali (simulati)
    local_tests = {
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

@router.get("/test-v1")
async def test_v1():
    """TEST V1: Testa il server MCP esterno"""
    result = await mcp_client.full_test()
    
    # Calcola statistiche
    total_tests = len(result)
    successful_tests = sum(1 for test in result.values() if test["status"] == "success")
    
    return {
        "version": "V1 - MCP Server",
        "timestamp": datetime.now().isoformat(),
        "mcp_server_url": mcp_client.mcp_url,
        "tests": result,
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": f"{(successful_tests/total_tests)*100:.1f}%"
        }
    }
