from fastapi import FastAPI

from app.api.search import router as search_router

app = FastAPI(
    title="Idea Finder API",
    version="1.0.0",
)

app.include_router(search_router)


@app.get("/")
def root():
    return {"message": "Idea Finder API Running 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}