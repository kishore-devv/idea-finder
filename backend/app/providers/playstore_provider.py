from google_play_scraper import search, app, reviews


class PlayStoreProvider:

    def search_apps(self, keyword: str, limit: int = 20):

        results = search(
            keyword,
            n_hits=limit,
            lang="en",
            country="us",
        )

        return results

    def get_app_details(self, app_id: str):

        return app(
            app_id,
            lang="en",
            country="us",
        )

    def get_reviews(self, app_id: str, limit: int = 100):

        result, _ = reviews(
            app_id,
            lang="en",
            country="us",
            count=limit,
        )

        return result