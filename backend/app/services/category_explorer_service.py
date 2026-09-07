from app.database.database import SessionLocal
from app.database.models import App
from app.services.app_filter_service import AppFilterService


class CategoryExplorerService:

    def explore(
        self,
        category: str,
        keyword: str | None = None,
        min_rating: float | None = None,
        max_rating: float | None = None,
        min_ratings: int | None = None,
        max_ratings: int | None = None,
        min_reviews: int | None = None,
        max_reviews: int | None = None,
        min_installs: int | None = None,
        max_installs: int | None = None,
        install_bucket: str | None = None,
        free: bool | None = None,
        contains_ads: bool | None = None,
        offers_iap: bool | None = None,
        developer: str | None = None,
        recently_updated_days: int | None = None,
        old_not_updated_days: int | None = None,
    ):

        db = SessionLocal()

        try:

            apps = db.query(App).filter(App.category.ilike(f"%{category}%")).all()

            filters = {
                "category": category,
                "keyword": keyword,
                "min_rating": min_rating,
                "max_rating": max_rating,
                "min_ratings": min_ratings,
                "max_ratings": max_ratings,
                "min_reviews": min_reviews,
                "max_reviews": max_reviews,
                "min_installs": min_installs,
                "max_installs": max_installs,
                "install_bucket": install_bucket,
                "free": free,
                "contains_ads": contains_ads,
                "offers_iap": offers_iap,
                "developer": developer,
                "recently_updated_days": recently_updated_days,
                "old_not_updated_days": old_not_updated_days,
            }

            filtered_apps = AppFilterService.filter_apps(
                apps,
                **filters,
            )

            return {
                "category": category,
                "total": len(filtered_apps),
                "apps": [
                    {
                        "app_id": app.app_id,
                        "title": app.title,
                        "developer": app.developer,
                        "category": app.category,
                        "score": app.score,
                        "ratings": app.ratings,
                        "reviews": app.reviews,
                        "installs": app.installs,
                        "real_installs": app.real_installs,
                        "free": app.free,
                        "contains_ads": app.contains_ads,
                        "offers_iap": app.offers_iap,
                        "last_updated": app.last_updated,
                        "icon": app.icon,
                        "url": app.url,
                    }
                    for app in filtered_apps
                ],
            }

        finally:
            db.close()
