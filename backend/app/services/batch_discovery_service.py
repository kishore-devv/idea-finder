from app.services.discovery_service import DiscoveryService


class BatchDiscoveryService:

    def __init__(self):
        self.discovery_service = DiscoveryService()

    def discover(self, keywords, limit=20):

        keyword_results = []

        unique_apps_map = {}

        total_results_found = 0

        for keyword in keywords:

            print(f"\nSearching for keyword: {keyword}")

            apps = self.discovery_service.search(keyword=keyword, limit=limit)

            total_results_found += len(apps)

            keyword_results.append(
                {
                    "keyword": keyword,
                    "apps_found": len(apps),
                    "apps": apps,
                }
            )

            # --------------------------------
            # Merge duplicate apps
            # --------------------------------

            for app in apps:

                app_id = app["app_id"]

                if app_id not in unique_apps_map:

                    unique_apps_map[app_id] = {
                        **app,
                        "found_by_keywords": [keyword],
                    }

                else:

                    unique_apps_map[app_id]["found_by_keywords"].append(keyword)

        unique_apps = list(unique_apps_map.values())

        return {
            "total_keywords": len(keywords),
            "total_results_found": total_results_found,
            "unique_apps_found": len(unique_apps),
            "duplicates_removed": (total_results_found - len(unique_apps)),
            "keyword_results": keyword_results,
            "unique_apps": unique_apps,
        }
