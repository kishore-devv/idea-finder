from fastapi import APIRouter
from pydantic import BaseModel

from app.services.automatic_query_discovery_service import (
    AutomaticQueryDiscoveryService,
)

router = APIRouter(
    prefix="/category-discovery",
    tags=["Category Discovery"],
)


class CategoryDiscoveryRequest(BaseModel):
    category: str
    limit: int = 20
    rounds: int = 3
    queries_per_round: int = 10


@router.post("")
def discover_category(request: CategoryDiscoveryRequest):
    service = AutomaticQueryDiscoveryService()

    return service.discover(
        category=request.category,
        limit=request.limit,
        rounds=request.rounds,
        queries_per_round=request.queries_per_round,
    )
