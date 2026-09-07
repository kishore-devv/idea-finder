from fastapi import FastAPI

from app.api.search import router as search_router
from app.database.database import engine, Base
from app.database import models

from app.api.analysis import router as analysis_router

from app.api.hidden_gems import router as hidden_gems_router

from app.api.market_analysis import router as market_analysis_router

from app.api.discovery import router as discovery_router

from app.api.category import router as category_router

from app.api.analyzer import router as analyzer_router

from app.api.category import router as category_router

from app.api.category_discovery import router as category_discovery_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Idea Finder API",
    version="1.0.0",
)


app.include_router(search_router)
app.include_router(analysis_router)
app.include_router(hidden_gems_router)
app.include_router(market_analysis_router)
app.include_router(discovery_router)
app.include_router(category_router)
app.include_router(analyzer_router)
app.include_router(category_router)
app.include_router(category_discovery_router)


@app.get("/")
def root():
    return {"message": "Idea Finder API Running 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}
