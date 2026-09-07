import re
from collections import Counter

from app.database.database import SessionLocal
from app.database.models import App
from app.providers.playstore_provider import PlayStoreProvider


class AutomaticQueryDiscoveryService:
    """
    Discovers new search queries from Google Play app data.

    Flow:
    category
      -> initial search
      -> collect titles/descriptions
      -> extract useful phrases
      -> search discovered phrases
      -> repeat
    """

    STOPWORDS = {
        "the",
        "and",
        "for",
        "with",
        "your",
        "you",
        "app",
        "apps",
        "free",
        "best",
        "online",
        "official",
        "new",
        "easy",
        "use",
        "used",
        "using",
        "get",
        "can",
        "this",
        "that",
        "from",
        "to",
        "of",
        "in",
        "on",
        "a",
        "an",
        "is",
        "it",
        "by",
        "or",
        "as",
        "at",
        "be",
        "all",
        "more",
        "one",
        "now",
    }

    def __init__(self):
        self.provider = PlayStoreProvider()

    def _tokenize(self, text: str):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        tokens = [
            token
            for token in text.split()
            if len(token) >= 3 and token not in self.STOPWORDS
        ]

        return tokens

    def _extract_queries(self, apps, max_queries: int = 10):
        """
        Extract data-driven 1-3 word phrases from app titles/descriptions.
        """

        unigram_counts = Counter()
        bigram_counts = Counter()
        trigram_counts = Counter()

        for app in apps:
            text = " ".join(
                filter(
                    None,
                    [
                        app.get("title"),
                        app.get("description"),
                    ],
                )
            )

            tokens = self._tokenize(text)

            # Avoid allowing one app with a huge description
            # to dominate the vocabulary.
            tokens = tokens[:300]

            unigram_counts.update(tokens)

            for i in range(len(tokens) - 1):
                bigram_counts.update([f"{tokens[i]} {tokens[i + 1]}"])

            for i in range(len(tokens) - 2):
                trigram_counts.update([f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}"])

        candidates = []

        for phrase, count in trigram_counts.items():
            if count >= 2:
                candidates.append((phrase, count, 3))

        for phrase, count in bigram_counts.items():
            if count >= 2:
                candidates.append((phrase, count, 2))

        for phrase, count in unigram_counts.items():
            if count >= 3:
                candidates.append((phrase, count, 1))

        # Prefer longer meaningful phrases, then frequency.
        candidates.sort(
            key=lambda item: (item[2], item[1]),
            reverse=True,
        )

        selected = []
        selected_normalized = set()

        for phrase, _, _ in candidates:
            normalized = phrase.strip().lower()

            if normalized in selected_normalized:
                continue

            # Don't generate queries that are simply one generic word.
            if len(normalized.split()) == 1 and len(normalized) < 5:
                continue

            selected.append(normalized)
            selected_normalized.add(normalized)

            if len(selected) >= max_queries:
                break

        return selected

    def discover(
        self,
        category: str,
        limit: int = 20,
        rounds: int = 3,
        queries_per_round: int = 10,
    ):
        db = SessionLocal()

        all_discovered = []
        seen_app_ids = set()
        seen_queries = set()

        try:
            # The category itself is the only initial seed.
            current_queries = [category]

            for round_number in range(1, rounds + 1):
                next_source_apps = []

                print(f"\n=== Discovery Round {round_number} ===")
                print(f"Queries: {current_queries}")

                for query in current_queries:
                    normalized_query = query.strip().lower()

                    if not normalized_query:
                        continue

                    if normalized_query in seen_queries:
                        continue

                    seen_queries.add(normalized_query)

                    try:
                        results = self.provider.search_apps(
                            query,
                            limit=limit,
                        )
                    except Exception as error:
                        print(f"Search failed for '{query}': {error}")
                        continue

                    for result in results:
                        app_id = result.get("appId")

                        if not app_id:
                            continue

                        if app_id in seen_app_ids:
                            continue

                        seen_app_ids.add(app_id)

                        try:
                            details = self.provider.get_app_details(app_id)
                        except Exception as error:
                            print(f"Details failed for {app_id}: {error}")
                            continue

                        actual_category = details.get("genre")

                        if not actual_category:
                            continue

                        # Verify that the app belongs to the
                        # requested category.
                        if category.lower() not in actual_category.lower():
                            continue

                        next_source_apps.append(details)

                        existing_app = (
                            db.query(App).filter(App.app_id == app_id).first()
                        )

                        if existing_app:
                            db_app = existing_app
                        else:
                            db_app = App(app_id=app_id)
                            db.add(db_app)

                        db_app.title = details.get("title")
                        db_app.developer = details.get("developer")
                        db_app.description = details.get("description")
                        db_app.category = actual_category
                        db_app.score = details.get("score")
                        db_app.ratings = details.get("ratings")
                        db_app.reviews = details.get("reviews")
                        db_app.installs = details.get("installs")
                        db_app.real_installs = details.get("realInstalls")
                        db_app.price = details.get("price")
                        db_app.free = details.get("free")
                        db_app.contains_ads = details.get("containsAds")
                        db_app.offers_iap = details.get("offersIAP")
                        db_app.iap_price = details.get("inAppProductPrice")
                        db_app.released = details.get("released")
                        db_app.last_updated = details.get("lastUpdatedOn")
                        db_app.icon = details.get("icon")
                        db_app.url = details.get("url")

                        db.commit()

                        all_discovered.append(
                            {
                                "app_id": app_id,
                                "title": details.get("title"),
                                "developer": details.get("developer"),
                                "category": actual_category,
                                "score": details.get("score"),
                                "ratings": details.get("ratings"),
                                "reviews": details.get("reviews"),
                                "installs": details.get("installs"),
                            }
                        )

                if not next_source_apps:
                    print("No new source apps found.")
                    break

                discovered_queries = self._extract_queries(
                    next_source_apps,
                    max_queries=queries_per_round,
                )

                current_queries = [
                    query for query in discovered_queries if query not in seen_queries
                ]

                if not current_queries:
                    print("No new queries discovered.")
                    break

            return {
                "category": category,
                "rounds": rounds,
                "queries_used": sorted(seen_queries),
                "queries_count": len(seen_queries),
                "discovered": len(all_discovered),
                "unique_apps": len(seen_app_ids),
                "apps": all_discovered,
            }

        finally:
            db.close()
