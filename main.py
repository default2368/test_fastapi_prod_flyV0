from fastapi import FastAPI

from modules.test import esegui_test_completo
#from modules.mcp import test_mcp, get_mcp_info, test_mcp_advanced, run_mcp_tool

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

