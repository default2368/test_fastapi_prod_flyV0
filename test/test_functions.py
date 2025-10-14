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

# Funzione di test per uso esterno
def test_tutte_funzioni():
    """Testa tutte le funzioni decorate e restituisce i risultati"""
    print("\n" + "="*50)
    print("TEST DI TUTTE LE FUNZIONI DECORATE")
    print("="*50)
    
    risultati = {
        "saluta": saluta(),
        "somma_semplice": somma_semplice()
    }
    
    return risultati
