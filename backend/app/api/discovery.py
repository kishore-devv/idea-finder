from fastapi import APIRouter
from pydantic import BaseModel

from app.services.batch_discovery_service import BatchDiscoveryService
from app.services.unique_app_processor import UniqueAppProcessor

router = APIRouter(prefix="/discover", tags=["Discovery"])


class BatchDiscoveryRequest(BaseModel):

    keywords: list[str]

    limit: int = 20


@router.post("/batch")
def batch_discover(request: BatchDiscoveryRequest):

    # --------------------------------
    # Initialize services
    # --------------------------------

    batch_service = BatchDiscoveryService()

    processor = UniqueAppProcessor()

    # --------------------------------
    # Step 1: Discover apps
    # --------------------------------

    discovery_result = batch_service.discover(
        keywords=request.keywords, limit=request.limit
    )

    # --------------------------------
    # Step 2: Get unique apps
    # --------------------------------

    unique_apps = discovery_result["unique_apps"]

    # --------------------------------
    # Step 3: Process unique apps
    # --------------------------------

    processing_result = processor.process(unique_apps)

    # --------------------------------
    # Return result
    # --------------------------------

    return {
        "total_keywords": len(request.keywords),
        "discovery": discovery_result,
        "processing": processing_result,
    }
