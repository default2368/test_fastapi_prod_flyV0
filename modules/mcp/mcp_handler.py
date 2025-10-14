from fastmcp import FastMCP
import asyncio

# Inizializza MCP
mcp = FastMCP("My FastAPI MCP Server")

@mcp.tool()
async def get_server_info():
    """Restituisce informazioni sul server MCP"""
    return {
        "server_name": "FastAPI MCP Integration",
        "version": "1.0.0",
        "status": "active"
    }

@mcp.tool()
async def calculate_sum(a: float, b: float):
    """Calcola la somma di due numeri"""
    return {"result": a + b, "operation": "sum"}

@mcp.tool()
async def echo_message(message: str):
    """Ripete il messaggio ricevuto"""
    return {"echo": message, "timestamp": "2024-01-01T00:00:00Z"}

# Funzioni di test per FastAPI
async def test_mcp():
    """Testa le funzioni MCP e restituisce i risultati"""
    print("\n" + "="*50)
    print("🚀 TEST MCP INTEGRATION")
    print("="*50)
    
    try:
        # Test delle funzioni MCP
        info = await get_server_info()
        sum_result = await calculate_sum(10, 5)
        echo_result = await echo_message("Ciao dal test MCP!")
        
        risultati = {
            "server_info": info,
            "calculation": sum_result,
            "echo_test": echo_result
        }
        
        print("✅ TEST MCP COMPLETATO CON SUCCESSO")
        print("="*50)
        
        return {
            "status": "success",
            "results": risultati
        }
        
    except Exception as e:
        print(f"❌ ERRORE MCP: {e}")
        print("="*50)
        return {
            "status": "error",
            "error": str(e)
        }

def get_mcp_info():
    """Restituisce informazioni base sul modulo MCP"""
    return {
        "module": "MCP Handler",
        "available_tools": ["get_server_info", "calculate_sum", "echo_message"],
        "description": "Modulo per l'integrazione MCP con FastAPI"
    }
