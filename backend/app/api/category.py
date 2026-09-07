from fastapi import APIRouter

from app.services.category_explorer_service import CategoryExplorerService

router = APIRouter(prefix="/category", tags=["Category Explorer"])


service = CategoryExplorerService()


@router.get("/apps")
def explore_category(
    category: str,
    min_rating: float | None = None,
    max_rating: float | None = None,
    min_ratings: int | None = None,
    min_reviews: int | None = None,
    min_installs: int | None = None,
    max_installs: int | None = None,
    free: bool | None = None,
    contains_ads: bool | None = None,
    offers_iap: bool | None = None,
    developer: str | None = None,
    recently_updated_days: int | None = None,
    old_not_updated_days: int | None = None,
):

    return service.explore(
        category=category,
        min_rating=min_rating,
        max_rating=max_rating,
        min_ratings=min_ratings,
        min_reviews=min_reviews,
        min_installs=min_installs,
        max_installs=max_installs,
        free=free,
        contains_ads=contains_ads,
        offers_iap=offers_iap,
        developer=developer,
        recently_updated_days=recently_updated_days,
        old_not_updated_days=old_not_updated_days,
    )
