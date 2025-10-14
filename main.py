from fastapi import FastAPI

app = FastAPI()

@app.get("/welcome")
async def welcome():
    return {"message": "Benvenuto nella mia app!"}

@app.get("/")
async def root():
    return {"info": "Vai su /welcome per il messaggio di benvenuto"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
