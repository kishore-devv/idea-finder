from app.services.discovery_service import DiscoveryService


class BatchDiscoveryService:

    def __init__(self):
        self.discovery_service = DiscoveryService()

    def discover(self, keywords, limit=20):

        # ---------------------------------------------
        # Keyword-level results
        # ---------------------------------------------

        results = []

        # ---------------------------------------------
        # Store unique apps using app_id as the key
        # ---------------------------------------------

        unique_apps = {}

        # ---------------------------------------------
        # Search each keyword
        # ---------------------------------------------

        for keyword in keywords:

            print(f"\nSearching for keyword: {keyword}")

            apps = self.discovery_service.search(keyword=keyword, limit=limit)

            # -----------------------------------------
            # Keep existing keyword-level results
            # -----------------------------------------

            results.append({"keyword": keyword, "apps_found": len(apps), "apps": apps})

            # -----------------------------------------
            # Build combined unique app collection
            # -----------------------------------------

            for app in apps:

                app_id = app.get("app_id")

                if not app_id:
                    continue

                # -------------------------------------
                # New unique app
                # -------------------------------------

                if app_id not in unique_apps:

                    unique_apps[app_id] = {**app, "found_by_keywords": [keyword]}

                # -------------------------------------
                # Existing app found by another keyword
                # -------------------------------------

                else:

                    found_keywords = unique_apps[app_id]["found_by_keywords"]

                    if keyword not in found_keywords:
                        found_keywords.append(keyword)

        # ---------------------------------------------
        # Convert dictionary to list
        # ---------------------------------------------

        combined_apps = list(unique_apps.values())

        # ---------------------------------------------
        # Calculate statistics
        # ---------------------------------------------

        total_results_found = sum(item["apps_found"] for item in results)

        unique_apps_found = len(combined_apps)

        duplicates_removed = total_results_found - unique_apps_found

        # ---------------------------------------------
        # Return both views
        # ---------------------------------------------

        return {
            "total_keywords": len(keywords),
            "total_results_found": total_results_found,
            "unique_apps_found": unique_apps_found,
            "duplicates_removed": duplicates_removed,
            "results": results,
            "unique_apps": combined_apps,
        }
