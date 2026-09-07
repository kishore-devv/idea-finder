from app.providers.playstore_provider import PlayStoreProvider


class AppSearchService:

    def __init__(self):
        self.provider = PlayStoreProvider()

    def search(self, keyword: str, limit: int = 20):

        results = self.provider.search_apps(
            keyword=keyword,
            limit=limit,
        )

        return results
