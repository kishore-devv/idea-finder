from app.services.app_search_service import AppSearchService
from app.services.app_relevance_service import AppRelevanceService
from app.services.app_filter_service import AppFilterService


class IntelligentDiscoveryService:

    def __init__(self):
        self.search_service = AppSearchService()
        self.relevance_service = AppRelevanceService()

    def discover(
        self,
        keyword: str,
        limit: int = 20,
        category: str | None = None,
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

        apps = self.search_service.search(
            keyword=keyword,
            limit=limit,
        )

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

        relevant_apps = self.relevance_service.filter_relevant_apps(
            keyword=keyword,
            apps=filtered_apps,
        )

        return {
            "keyword": keyword,
            "filters": filters,
            "total_candidates_found": len(apps),
            "filtered_apps_found": len(filtered_apps),
            "relevant_apps_found": len(relevant_apps),
            "relevant_apps": relevant_apps,
        }
