from fastapi import FastAPI

from modules.test import esegui_test_completo
from modules.mcp import test_mcp, get_mcp_info, test_mcp_advanced

app = FastAPI()

@app.get("/welcome")
async def welcome():
    return {"message": "Benvenuto nella mia app!"}

@app.get("/")
async def root():
    return {"info": "Vai su /welcome per il messaggio di benvenuto"}

@app.get("/test")
async def test_endpoint():
    """Unico endpoint per testare tutte le funzioni decorate"""
    risultati = esegui_test_completo()
    
    return {
        "status": "success",
        "risultati": risultati,
        "message": "Controlla i log del server per vedere il decoratore in azione!"
    }

@app.get("/test-mcp")
async def test_mcp_endpoint():
    """Testa l'integrazione MCP"""
    risultati = await test_mcp()
    
    return {
        "endpoint": "test-mcp",
        "mcp_test": risultati
    }

@app.get("/mcp-info")
async def mcp_info():
    """Restituisce informazioni sul modulo MCP"""
    info = get_mcp_info()
    return {
        "module_info": info
    }

@app.get("/test-mcp")
async def test_mcp_endpoint():
    """Testa l'integrazione MCP (versione base)"""
    risultati = await test_mcp()
    
    return {
        "endpoint": "test-mcp",
        "mcp_test": risultati
    }

@app.get("/test-mcp-advanced")
async def test_mcp_advanced_endpoint():
    """Testa l'integrazione MCP (versione avanzata)"""
    risultati = await test_mcp_advanced()
    
    return {
        "endpoint": "test-mcp-advanced", 
        "mcp_test": risultati
    }

@app.get("/mcp-info")
async def mcp_info():
    """Restituisce informazioni sul modulo MCP"""
    info = get_mcp_info()
    return {
        "module_info": info
    }
