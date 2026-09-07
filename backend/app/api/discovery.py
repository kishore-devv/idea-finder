from fastapi import APIRouter
from pydantic import BaseModel

from app.services.batch_discovery_service import BatchDiscoveryService

from app.services.intelligent_discovery_service import IntelligentDiscoveryService

router = APIRouter(
    prefix="/discover",
    tags=["Discovery"],
)


# --------------------------------
# Batch Discovery Request
# --------------------------------


class BatchDiscoveryRequest(BaseModel):

    keywords: list[str]

    limit: int = 20


# --------------------------------
# Intelligent Discovery Request
# --------------------------------


class IntelligentDiscoveryRequest(BaseModel):

    keyword: str

    limit: int = 20


# --------------------------------
# Existing Multi-keyword Discovery
# --------------------------------


@router.post("/batch")
def batch_discover(request: BatchDiscoveryRequest):

    service = BatchDiscoveryService()

    results = service.discover(
        keywords=request.keywords,
        limit=request.limit,
    )

    return {
        "total_keywords": len(request.keywords),
        "results": results,
    }


# --------------------------------
# Intelligent Discovery
# --------------------------------


@router.post("/intelligent")
def intelligent_discover(request: IntelligentDiscoveryRequest):

    service = IntelligentDiscoveryService()

    results = service.discover(
        keyword=request.keyword,
        limit=request.limit,
    )

    return results
