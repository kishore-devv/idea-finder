from fastapi import APIRouter
from pydantic import BaseModel

from app.services.batch_discovery_service import BatchDiscoveryService
from app.services.intelligent_discovery_service import IntelligentDiscoveryService

router = APIRouter(
    prefix="/discover",
    tags=["Discovery"],
)


class BatchDiscoveryRequest(BaseModel):
    keywords: list[str]
    limit: int = 20


class IntelligentDiscoveryRequest(BaseModel):
    keyword: str
    limit: int = 20

    category: str | None = None

    min_rating: float | None = None
    max_rating: float | None = None

    min_ratings: int | None = None
    max_ratings: int | None = None

    min_reviews: int | None = None
    max_reviews: int | None = None

    min_installs: int | None = None
    max_installs: int | None = None

    install_bucket: str | None = None

    free: bool | None = None
    contains_ads: bool | None = None
    offers_iap: bool | None = None

    developer: str | None = None

    recently_updated_days: int | None = None
    old_not_updated_days: int | None = None


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


@router.post("/intelligent")
def intelligent_discover(request: IntelligentDiscoveryRequest):

    service = IntelligentDiscoveryService()

    return service.discover(
        keyword=request.keyword,
        limit=request.limit,
        category=request.category,
        min_rating=request.min_rating,
        max_rating=request.max_rating,
        min_ratings=request.min_ratings,
        max_ratings=request.max_ratings,
        min_reviews=request.min_reviews,
        max_reviews=request.max_reviews,
        min_installs=request.min_installs,
        max_installs=request.max_installs,
        install_bucket=request.install_bucket,
        free=request.free,
        contains_ads=request.contains_ads,
        offers_iap=request.offers_iap,
        developer=request.developer,
        recently_updated_days=request.recently_updated_days,
        old_not_updated_days=request.old_not_updated_days,
    )
