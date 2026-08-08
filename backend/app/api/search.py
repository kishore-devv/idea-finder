from fastapi import APIRouter, Query

from app.services.discovery_service import DiscoveryService

router = APIRouter(prefix="/search", tags=["Search"])

service = DiscoveryService()


@router.get("/")
def search_apps(
    q: str,
    limit: int = Query(20, ge=1, le=100),
):
    return service.search(
        keyword=q,
        limit=limit,
    )


@router.get("/app/{app_id}")
def get_app_details(app_id: str):

    return service.get_details(app_id)


@router.get("/app/{app_id}/reviews")
def get_app_reviews(app_id: str, count: int = 100):

    return service.get_reviews(
        app_id=app_id,
        count=count,
    )


# @router.get("/analysis/{app_id}")
# def get_app_analysis(app_id: str, count: int = 100):

#     return service.get_reviews(
#         app_id=app_id,
#         count=count,
#     )
