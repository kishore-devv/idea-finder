import re
from collections import Counter

from app.database.database import SessionLocal
from app.database.models import App
from app.providers.playstore_provider import PlayStoreProvider
from app.services.app_filter_service import AppFilterService


class AutomaticQueryDiscoveryService:
    """
    Automatically discovers Google Play apps using data-driven queries.

    Flow:

        category
            ↓
        initial Google Play search
            ↓
        fetch app details
            ↓
        category + user filters
            ↓
        save matching apps
            ↓
        extract vocabulary from discovered apps
            ↓
        generate new queries
            ↓
        repeat

    The same AppFilterService is used by discovery and Category Explorer.
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

    # ---------------------------------------------------------
    # Tokenization
    # ---------------------------------------------------------

    def _tokenize(self, text: str):

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        tokens = [
            token
            for token in text.split()
            if len(token) >= 3 and token not in self.STOPWORDS
        ]

        return tokens

    # ---------------------------------------------------------
    # Automatic query extraction
    # ---------------------------------------------------------

    def _extract_queries(
        self,
        apps,
        max_queries: int = 10,
    ):
        """
        Extract data-driven 1-3 word phrases from discovered apps.
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

            # Prevent very long descriptions from dominating.
            tokens = tokens[:300]

            unigram_counts.update(tokens)

            for i in range(len(tokens) - 1):

                bigram_counts.update([f"{tokens[i]} {tokens[i + 1]}"])

            for i in range(len(tokens) - 2):

                trigram_counts.update(
                    [f"{tokens[i]} " f"{tokens[i + 1]} " f"{tokens[i + 2]}"]
                )

        candidates = []

        # -----------------------------------------------------
        # Trigrams
        # -----------------------------------------------------

        for phrase, count in trigram_counts.items():

            if count >= 2:

                candidates.append(
                    (
                        phrase,
                        count,
                        3,
                    )
                )

        # -----------------------------------------------------
        # Bigrams
        # -----------------------------------------------------

        for phrase, count in bigram_counts.items():

            if count >= 2:

                candidates.append(
                    (
                        phrase,
                        count,
                        2,
                    )
                )

        # -----------------------------------------------------
        # Unigrams
        # -----------------------------------------------------

        for phrase, count in unigram_counts.items():

            if count >= 3:

                candidates.append(
                    (
                        phrase,
                        count,
                        1,
                    )
                )

        # Prefer longer phrases first,
        # then frequency.
        candidates.sort(
            key=lambda item: (
                item[2],
                item[1],
            ),
            reverse=True,
        )

        selected = []
        selected_normalized = set()

        for phrase, _, _ in candidates:

            normalized = phrase.strip().lower()

            if not normalized:
                continue

            if normalized in selected_normalized:
                continue

            # Avoid extremely short single-word queries.
            if len(normalized.split()) == 1 and len(normalized) < 5:
                continue

            selected.append(normalized)

            selected_normalized.add(normalized)

            if len(selected) >= max_queries:
                break

        return selected

    # ---------------------------------------------------------
    # Main discovery
    # ---------------------------------------------------------

    def discover(
        self,
        category: str,
        limit: int = 20,
        rounds: int = 3,
        queries_per_round: int = 10,
        # Filters
        keyword: str | None = None,
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

        db = SessionLocal()

        all_discovered = []

        seen_app_ids = set()

        seen_queries = set()

        try:

            # -------------------------------------------------
            # Initial seed
            # -------------------------------------------------

            current_queries = [category]

            # -------------------------------------------------
            # Filters shared with AppFilterService
            # -------------------------------------------------

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

            # -------------------------------------------------
            # Discovery rounds
            # -------------------------------------------------

            for round_number in range(
                1,
                rounds + 1,
            ):

                next_source_apps = []

                print(f"\n=== Discovery Round " f"{round_number} ===")

                print(f"Queries: {current_queries}")

                # -------------------------------------------------
                # Search queries
                # -------------------------------------------------

                for query in current_queries:

                    normalized_query = query.strip().lower()

                    if not normalized_query:
                        continue

                    if normalized_query in seen_queries:
                        continue

                    seen_queries.add(normalized_query)

                    print(f"Searching Google Play: " f"{query}")

                    try:

                        results = self.provider.search_apps(
                            query,
                            limit=limit,
                        )

                    except Exception as error:

                        print(f"Search failed for " f"'{query}': {error}")

                        continue

                    # -------------------------------------------------
                    # Process search results
                    # -------------------------------------------------

                    for result in results:

                        app_id = result.get("appId")

                        if not app_id:
                            continue

                        if app_id in seen_app_ids:
                            continue

                        # Mark candidate as seen before
                        # fetching details to prevent
                        # repeated API requests.
                        seen_app_ids.add(app_id)

                        # -------------------------------------------------
                        # Fetch full details
                        # -------------------------------------------------

                        try:

                            details = self.provider.get_app_details(app_id)

                        except Exception as error:

                            print(f"Details failed for " f"{app_id}: {error}")

                            continue

                        # -------------------------------------------------
                        # Apply ALL filters
                        # -------------------------------------------------

                        if not AppFilterService.matches(
                            details,
                            **filters,
                        ):
                            continue

                        # This app passed all filters.
                        next_source_apps.append(details)

                        # -------------------------------------------------
                        # Save / update database
                        # -------------------------------------------------

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

                        db_app.category = details.get("genre")

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

                        # -------------------------------------------------
                        # Response entry
                        # -------------------------------------------------

                        all_discovered.append(
                            {
                                "app_id": app_id,
                                "title": details.get("title"),
                                "developer": details.get("developer"),
                                "category": details.get("genre"),
                                "score": details.get("score"),
                                "ratings": details.get("ratings"),
                                "reviews": details.get("reviews"),
                                "installs": details.get("installs"),
                                "real_installs": (details.get("realInstalls")),
                                "free": details.get("free"),
                                "contains_ads": (details.get("containsAds")),
                                "offers_iap": (details.get("offersIAP")),
                                "last_updated": (details.get("lastUpdatedOn")),
                            }
                        )

                # ---------------------------------------------------------
                # No matching apps
                # ---------------------------------------------------------

                if not next_source_apps:

                    print("No matching source apps found.")

                    break

                # ---------------------------------------------------------
                # Discover new queries from matching apps
                # ---------------------------------------------------------

                discovered_queries = self._extract_queries(
                    next_source_apps,
                    max_queries=queries_per_round,
                )

                current_queries = [
                    query for query in discovered_queries if query not in seen_queries
                ]

                # ---------------------------------------------------------
                # No new queries
                # ---------------------------------------------------------

                if not current_queries:

                    print("No new queries discovered.")

                    break

            # ---------------------------------------------------------
            # Final response
            # ---------------------------------------------------------

            return {
                "category": category,
                "rounds": rounds,
                "queries_used": sorted(seen_queries),
                "queries_count": len(seen_queries),
                "discovered": len(all_discovered),
                "unique_apps": len(all_discovered),
                "filters": {
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
                    "recently_updated_days": (recently_updated_days),
                    "old_not_updated_days": (old_not_updated_days),
                },
                "apps": all_discovered,
            }

        finally:

            db.close()
