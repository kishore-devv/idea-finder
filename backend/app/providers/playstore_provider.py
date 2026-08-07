from google_play_scraper import search


class PlayStoreProvider:

    def search_apps(self, keyword: str, limit: int = 20):

        return search(
            keyword,
            n_hits=limit,
            lang="en",
            country="us",
        )