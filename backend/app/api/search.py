from fastapi import APIRouter

from app.services.discovery_service import DiscoveryService


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

service = DiscoveryService()


@router.get("/")
def search_apps(q: str, limit: int = 20):

    return service.search(
        keyword=q,
        limit=limit,
    )