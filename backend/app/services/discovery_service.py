from app.providers.playstore_provider import PlayStoreProvider


class DiscoveryService:

    def __init__(self):
        self.provider = PlayStoreProvider()

    def search(self, keyword: str, limit: int = 20):

        apps = self.provider.search_apps(keyword, limit=limit)

        results = []

        for app in apps:

            app_id = app.get("appId")

            if not app_id:
                print("Skipping result without app ID")
                continue

            results.append(
                {
                    "app_id": app_id,
                    "title": app.get("title"),
                    "score": app.get("score"),
                    "installs": app.get("installs"),
                }
            )

        return results
