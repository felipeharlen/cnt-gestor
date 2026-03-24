from fastapi import FastAPI

app = FastAPI(title = "CNT Gestor API")

@app.get("/")
def root():
    return {"status": "ok"}