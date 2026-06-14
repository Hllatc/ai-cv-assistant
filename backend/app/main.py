from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI CV & Job Assistant",
    description="RAG-based CV analyzer and job matcher",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "AI CV Assistant API is running"}