from app.providers.playstore_provider import PlayStoreProvider


class DiscoveryService:

    def __init__(self):
        self.provider = PlayStoreProvider()

    def search(self, keyword: str, limit: int = 20):

        apps = self.provider.search_apps(
            keyword=keyword,
            limit=limit,
        )

        response = []

        for app in apps:

            response.append(
                {
                    "app_id": app.get("appId"),
                    "title": app.get("title"),
                    "developer": app.get("developer"),
                    "score": app.get("score"),
                    "installs": app.get("installs"),
                    "icon": app.get("icon"),
                }
            )

        return response