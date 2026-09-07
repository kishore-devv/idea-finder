from app.services.app_search_service import AppSearchService

from app.services.app_relevance_service import AppRelevanceService


class IntelligentDiscoveryService:

    def __init__(self):

        self.search_service = AppSearchService()

        self.relevance_service = AppRelevanceService()

    def discover(
        self,
        keyword: str,
        limit: int = 20,
    ):

        # --------------------------------
        # Step 1: Search candidate apps
        # --------------------------------

        apps = self.search_service.search(
            keyword=keyword,
            limit=limit,
        )

        print(f"Found {len(apps)} candidate apps")

        # --------------------------------
        # Step 2: Filter relevant apps
        # --------------------------------

        relevant_apps = self.relevance_service.filter_relevant_apps(
            keyword=keyword,
            apps=apps,
        )

        # --------------------------------
        # Step 3: Return results
        # --------------------------------

        return {
            "keyword": keyword,
            "total_candidates_found": len(apps),
            "relevant_apps_found": len(relevant_apps),
            "relevant_apps": relevant_apps,
        }
