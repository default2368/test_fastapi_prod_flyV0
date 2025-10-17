from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Import routes organizzate
from modules.routes import mcp, system_info, claude
from modules.test import esegui_test_completo

app = FastAPI(
    title="MCP System API",
    description="Sistema integrato FastAPI + MCP Server",
    version="2.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes organizzate
app.include_router(mcp.router)
app.include_router(system_info.router)

# ===== ENDPOINTS PRINCIPALI SEMPLIFICATI =====

@app.get("/", include_in_schema=False)
async def root():
    """Redirect alla documentazione API"""
    return RedirectResponse(url="/docs")

@app.get("/welcome")
async def welcome():
    """Endpoint di benvenuto"""
    return {
        "message": "Benvenuto nel Sistema MCP!",
        "version": "2.0.0",
        "description": "Sistema integrato FastAPI + MCP Server"
    }

@app.get("/test")
async def test_endpoint():
    """Testa le funzioni decorate locali"""
    risultati = esegui_test_completo()
    
    return {
        "status": "success",
        "risultati": risultati,
        "message": "Controlla i log del server per vedere il decoratore in azione!"
    }

@app.get("/docs-overview", include_in_schema=False)
async def docs_overview():
    """Panoramica degli endpoints disponibili"""
    return {
        "app": {
            "description": "Endpoints principali dell'applicazione",
            "endpoints": {
                "GET /": "Redirect alla documentazione",
                "GET /welcome": "Messaggio di benvenuto", 
                "GET /test": "Test funzioni decorate locali",
                "GET /docs": "Documentazione automatica Swagger",
                "GET /docs-overview": "Questa panoramica"
            }
        },
        "system": {
            "description": "Endpoints di sistema e monitoraggio",
            "endpoints": {
                "GET /system/health": "Health check completo sistema",
                "GET /system/status": "Status riepilogativo",
                "GET /system/test-v0": "Test completo FastAPI (V0)",
                "GET /system/test-v1": "Test completo MCP Server (V1)"
            }
        },
        "mcp": {
            "description": "Endpoints per il server MCP esterno",
            "endpoints": {
                "GET /mcp/test": "Test connessione MCP Server",
                "GET /mcp/tools": "Lista tools disponibili MCP",
                "GET /mcp/full-test": "Test completo MCP Server", 
                "GET /mcp/health": "Health check MCP Server"
            }
        }
    }

# Health check compatibilità (mantenimento retrocompatibilità)
@app.get("/health")
async def health_legacy():
    """Health check legacy - usa /system/health per la versione nuova"""
    from modules.routes.system_info import health_check
    return await health_check()

@app.get("/test-mcp")
async def test_mcp_legacy():
    """Test MCP legacy - usa /mcp/test per la versione nuova"""
    from modules.routes.mcp import test_mcp_connection
    return await test_mcp_connection()

@app.get("/test-v0")
async def test_v0_legacy():
    """Test V0 legacy - usa /system/test-v0 per la versione nuova"""
    from modules.routes.system_info import test_v0
    return await test_v0()

@app.get("/test-v1") 
async def test_v1_legacy():
    """Test V1 legacy - usa /system/test-v1 per la versione nuova"""
    from modules.routes.system_info import test_v1
    return await test_v1()

@app.get("/status")
async def status_legacy():
    """Status legacy - usa /system/status per la versione nuova"""
    from modules.routes.system_info import overall_status
    return await overall_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
