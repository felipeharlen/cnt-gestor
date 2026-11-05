from fastapi import FastAPI
from src.api.health import router as health_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API running"}

app.include_router(health_router, tags=["Health"])