from app.providers.playstore_provider import PlayStoreProvider
from app.database.database import SessionLocal
from app.database.models import App, Review


class DiscoveryService:

    def __init__(self):

        self.provider = PlayStoreProvider()

    def search(self, keyword: str):

        apps = self.provider.search_apps(keyword)

        db = SessionLocal()

        saved_apps = []

        try:

            for result in apps:

                app_id = result["appId"]

                print(f"Processing: {result['title']}")

                # --------------------------------
                # Get full app details
                # --------------------------------

                details = self.provider.get_app_details(app_id)

                # --------------------------------
                # Save app
                # --------------------------------

                existing_app = (
                    db.query(App)
                    .filter(App.app_id == app_id)
                    .first()
                )

                if existing_app:

                    db_app = existing_app

                else:

                    db_app = App(
                        app_id=app_id,
                    )

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
                db_app.offers_iap = details.get("offersIAP")
                db_app.iap_price = details.get("inAppProductPrice")
                db_app.released = details.get("released")
                db_app.last_updated = details.get("lastUpdatedOn")
                db_app.icon = details.get("icon")
                db_app.url = details.get("url")

                db.commit()

                # --------------------------------
                # Get reviews
                # --------------------------------

                app_reviews = self.provider.get_reviews(
                    app_id,
                    limit=100,
                )

                print(
                    f"Found {len(app_reviews)} reviews"
                )

                # --------------------------------
                # Save reviews
                # --------------------------------

                for review in app_reviews:

                    review_id = review.get("reviewId")

                    if not review_id:
                        continue

                    existing_review = (
                        db.query(Review)
                        .filter(
                            Review.review_id == review_id
                        )
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

                db.commit()

                saved_apps.append(
                    {
                        "app_id": app_id,
                        "title": details.get("title"),
                        "score": details.get("score"),
                        "installs": details.get("installs"),
                        "reviews_scraped": len(app_reviews),
                    }
                )

        finally:

            db.close()

        return saved_apps