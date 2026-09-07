from google_play_scraper.exceptions import NotFoundError

from app.providers.playstore_provider import PlayStoreProvider
from app.database.database import SessionLocal
from app.database.models import App, Review


class UniqueAppProcessor:

    def __init__(self):

        self.provider = PlayStoreProvider()

    def process(self, unique_apps):

        db = SessionLocal()

        processed_apps = []

        created_count = 0
        updated_count = 0
        failed_count = 0

        try:

            total_apps = len(unique_apps)

            print(f"\nTotal unique apps to process: " f"{total_apps}")

            for index, app in enumerate(unique_apps, start=1):

                app_id = app["app_id"]
                title = app.get("title")

                print(f"\n[{index}/{total_apps}] " f"Processing: {title}")

                try:

                    # --------------------------------
                    # Check if app already exists
                    # --------------------------------

                    existing_app = db.query(App).filter(App.app_id == app_id).first()

                    is_new_app = existing_app is None

                    # --------------------------------
                    # Get full app details
                    # --------------------------------

                    details = self.provider.get_app_details(app_id)

                    # --------------------------------
                    # Create or update app
                    # --------------------------------

                    if existing_app:

                        db_app = existing_app
                        updated_count += 1

                    else:

                        db_app = App(app_id=app_id)

                        db.add(db_app)

                        created_count += 1

                    # --------------------------------
                    # Update app fields
                    # --------------------------------

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
                    db_app.contains_ads = details.get("containsAds", False)
                    db_app.offers_iap = details.get("offersIAP")
                    db_app.iap_price = details.get("inAppProductPrice")
                    db_app.released = details.get("released")
                    db_app.last_updated = details.get("lastUpdatedOn")
                    db_app.icon = details.get("icon")
                    db_app.url = details.get("url")

                    # Save app first
                    db.commit()

                    # --------------------------------
                    # Fetch reviews
                    # --------------------------------

                    try:

                        app_reviews = self.provider.get_reviews(app_id, limit=100)

                        print(f"Found " f"{len(app_reviews)} reviews")

                    except Exception as error:

                        print(f"Could not fetch reviews " f"for {app_id}: {error}")

                        app_reviews = []

                    # --------------------------------
                    # Save only new reviews
                    # --------------------------------

                    new_reviews_count = 0

                    for review in app_reviews:

                        review_id = review.get("reviewId")

                        if not review_id:
                            continue

                        existing_review = (
                            db.query(Review)
                            .filter(Review.review_id == review_id)
                            .first()
                        )

                        if existing_review:
                            continue

                        db_review = Review(
                            review_id=review_id,
                            app_id=app_id,
                            user=review.get("userName"),
                            score=review.get("score"),
                            text=review.get("content"),
                            date=str(review.get("at")),
                            thumbs_up=review.get("thumbsUpCount"),
                            version=review.get("reviewCreatedVersion"),
                        )

                        db.add(db_review)

                        new_reviews_count += 1

                    db.commit()

                    # --------------------------------
                    # Add processing result
                    # --------------------------------

                    processed_apps.append(
                        {
                            "app_id": app_id,
                            "title": details.get("title"),
                            "status": ("created" if is_new_app else "updated"),
                            "reviews_fetched": len(app_reviews),
                            "new_reviews_saved": (new_reviews_count),
                            "found_by_keywords": (app.get("found_by_keywords", [])),
                        }
                    )

                except NotFoundError:

                    print(f"Skipping {app_id}: " f"App not found")

                    db.rollback()

                    failed_count += 1

                    processed_apps.append(
                        {
                            "app_id": app_id,
                            "title": title,
                            "status": "not_found",
                        }
                    )

                except Exception as error:

                    print(f"Error processing " f"{app_id}: {error}")

                    db.rollback()

                    failed_count += 1

                    processed_apps.append(
                        {
                            "app_id": app_id,
                            "title": title,
                            "status": "failed",
                            "error": str(error),
                        }
                    )

        finally:

            db.close()

        return {
            "total_unique_apps": len(unique_apps),
            "created": created_count,
            "updated": updated_count,
            "failed": failed_count,
            "apps": processed_apps,
        }
