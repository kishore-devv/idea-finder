from fastapi import APIRouter
from pydantic import BaseModel

from app.services.batch_discovery_service import BatchDiscoveryService

router = APIRouter(prefix="/discover", tags=["Discovery"])


class BatchDiscoveryRequest(BaseModel):

    keywords: list[str]

    limit: int = 20


@router.post("/batch")
def batch_discover(request: BatchDiscoveryRequest):

    service = BatchDiscoveryService()

    results = service.discover(keywords=request.keywords, limit=request.limit)

    return {"total_keywords": len(request.keywords), "results": results}
