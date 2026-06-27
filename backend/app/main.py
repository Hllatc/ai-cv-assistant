from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.routes import router as api_router

from app.db.database import Base, engine

# Models import 
from app.models.cv import CV
from app.models.user import User

from app.db.vector_store import init_qdrant

Base.metadata.create_all(bind=engine)


from app.services.cv_vector_service import init_qdrant


app = FastAPI(
    title="AI CV & Job Assistant",
    description="RAG-based CV analyzer and job matcher",
    version="1.0.0"
)
@app.on_event("startup")
def startup():
    init_qdrant()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(api_router, prefix="/api", tags=["API"])

@app.get("/")
def root():
    return {"message": "AI CV Assistant API is running"}
