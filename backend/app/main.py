from fastapi import FastAPI

from app.api.search import router as search_router
from app.database.database import engine, Base
from app.database import models

from app.api.analysis import router as analysis_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Idea Finder API",
    version="1.0.0",
)


app.include_router(search_router)
app.include_router(analysis_router)


@app.get("/")
def root():
    return {
        "message": "Idea Finder API Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }