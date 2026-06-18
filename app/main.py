from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.database.db import engine, Base
import app.database.models

app = FastAPI(title="RAG Backend API")

#now we create the tables(models)
Base.metadata.create_all(bind=engine)

app.include_router(upload_router)

@app.get("/")
def root():
    return {
        "message": "RAG API"}

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }