from app.database.database import SessionLocal
from app.database.models import App
from app.providers.playstore_provider import PlayStoreProvider


class CategoryDiscoveryService:

    def __init__(self):
        self.provider = PlayStoreProvider()

    def discover(
        self,
        category: str,
        queries: list[str],
        limit: int = 20,
    ):
        db = SessionLocal()

        discovered = []
        skipped = 0
        duplicates = 0

        try:

            # Use multiple discovery queries supplied by the caller.
            # No hardcoded category keyword map is used here.
            seen_app_ids = set()

            for query in queries:

                results = self.provider.search_apps(
                    query,
                    limit=limit,
                )

                for result in results:

                    app_id = result.get("appId")

                    if not app_id:
                        skipped += 1
                        continue

                    # Deduplicate during this discovery run.
                    if app_id in seen_app_ids:
                        duplicates += 1
                        continue

                    seen_app_ids.add(app_id)

                    try:
                        details = self.provider.get_app_details(app_id)

                    except Exception as error:
                        print(f"Could not fetch details for " f"{app_id}: {error}")
                        skipped += 1
                        continue

                    actual_category = details.get("genre")

                    # Verify the actual Play Store category.
                    if not actual_category:
                        skipped += 1
                        continue

                    if category.lower() not in actual_category.lower():
                        skipped += 1
                        continue

                    existing_app = db.query(App).filter(App.app_id == app_id).first()

                    if existing_app:
                        duplicates += 1
                        continue

                    db_app = App(
                        app_id=app_id,
                        title=details.get("title"),
                        developer=details.get("developer"),
                        description=details.get("description"),
                        category=actual_category,
                        score=details.get("score"),
                        ratings=details.get("ratings"),
                        reviews=details.get("reviews"),
                        installs=details.get("installs"),
                        real_installs=details.get("realInstalls"),
                        price=details.get("price"),
                        free=details.get("free"),
                        contains_ads=details.get("containsAds"),
                        offers_iap=details.get("offersIAP"),
                        iap_price=details.get("inAppProductPrice"),
                        released=details.get("released"),
                        last_updated=details.get("lastUpdatedOn"),
                        icon=details.get("icon"),
                        url=details.get("url"),
                    )

                    db.add(db_app)
                    db.commit()

                    discovered.append(
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

            return {
                "requested_category": category,
                "queries_used": queries,
                "discovered": len(discovered),
                "duplicates": duplicates,
                "skipped": skipped,
                "apps": discovered,
            }

        finally:
            db.close()
