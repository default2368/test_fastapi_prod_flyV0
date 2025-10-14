from fastapi import FastAPI

app = FastAPI()

@app.get("/welcome")
async def welcome():
    return {"message": "Benvenuto nella mia app!"}

@app.get("/")
async def root():
    return {"info": "Vai su /welcome per il messaggio di benvenuto"}

# Decoratore per logging
def logga_chiamata(func):
    def wrapper():
        print(f"▶️ INIZIO {func.__name__}")
        risultato = func()
        print(f"⏹️  FINE {func.__name__} → {risultato}")
        return risultato
    return wrapper

# Funzioni con decoratore
@logga_chiamata
def saluta():
    return "Ciao Mondo!"

@logga_chiamata
def somma_semplice():
    return 5 + 3
    
@app.get("/test-decoratore")
async def test_decoratore():
    # Test delle funzioni con decoratore
    risultato_saluta = saluta()
    risultato_somma = somma_semplice()
    
    return {
        "saluta": risultato_saluta,
        "somma": risultato_somma,
        "message": "Guarda i log del server per vedere il decoratore in azione!"
    }

@app.get("/direct-call")
async def direct_call():
    """Chiama direttamente le funzioni decorate"""
    print("\n" + "="*50)
    print("CHIAMATA DIRETTA DA FASTAPI")
    print("="*50)
    
    saluta()
    somma_semplice()
    
    return {"status": "Funzioni chiamate - controlla i log"}
