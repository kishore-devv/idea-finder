from datetime import datetime, timedelta

from app.database.database import SessionLocal
from app.database.models import App


class CategoryExplorerService:

    def explore(
        self,
        category: str,
        min_rating: float | None = None,
        max_rating: float | None = None,
        min_ratings: int | None = None,
        min_reviews: int | None = None,
        min_installs: int | None = None,
        max_installs: int | None = None,
        free: bool | None = None,
        contains_ads: bool | None = None,
        offers_iap: bool | None = None,
        developer: str | None = None,
        recently_updated_days: int | None = None,
        old_not_updated_days: int | None = None,
    ):

        db = SessionLocal()

        try:

            query = db.query(App).filter(App.category.ilike(f"%{category}%"))

            # Rating
            if min_rating is not None:
                query = query.filter(App.score >= min_rating)

            if max_rating is not None:
                query = query.filter(App.score <= max_rating)

            # Number of ratings
            if min_ratings is not None:
                query = query.filter(App.ratings >= min_ratings)

            # Number of reviews
            if min_reviews is not None:
                query = query.filter(App.reviews >= min_reviews)

            # Free / Paid
            if free is not None:
                query = query.filter(App.free == free)

            # Contains ads
            if contains_ads is not None:
                query = query.filter(App.contains_ads == contains_ads)

            # In-app purchases
            if offers_iap is not None:
                query = query.filter(App.offers_iap == offers_iap)

            # Developer
            if developer:
                query = query.filter(App.developer.ilike(f"%{developer}%"))

            # Installs
            if min_installs is not None:
                query = query.filter(App.real_installs >= min_installs)

            if max_installs is not None:
                query = query.filter(App.real_installs <= max_installs)

            apps = query.all()

            # -------------------------------------------------
            # Date filtering
            # Only apply date logic when requested
            # -------------------------------------------------

            if recently_updated_days is not None or old_not_updated_days is not None:

                now = datetime.utcnow()
                filtered_apps = []

                for app in apps:

                    # If date filtering was requested but this
                    # app has no update date, skip it.
                    if not app.last_updated:
                        continue

                    updated_date = None

                    try:
                        updated_date = datetime.strptime(app.last_updated, "%Y-%m-%d")
                    except ValueError:

                        try:
                            updated_date = datetime.fromisoformat(app.last_updated)
                        except ValueError:
                            pass

                    if updated_date is None:
                        continue

                    # Recently updated
                    if recently_updated_days is not None:

                        cutoff = now - timedelta(days=recently_updated_days)

                        if updated_date < cutoff:
                            continue

                    # Old / not updated
                    if old_not_updated_days is not None:

                        cutoff = now - timedelta(days=old_not_updated_days)

                        if updated_date >= cutoff:
                            continue

                    filtered_apps.append(app)

            else:
                # No date filter requested.
                # Keep all matching apps.
                filtered_apps = apps

            # -------------------------------------------------
            # Response
            # -------------------------------------------------

            return {
                "category": category,
                "total": len(filtered_apps),
                "apps": [
                    {
                        "app_id": app.app_id,
                        "title": app.title,
                        "developer": app.developer,
                        "category": app.category,
                        "score": app.score,
                        "ratings": app.ratings,
                        "reviews": app.reviews,
                        "installs": app.installs,
                        "real_installs": app.real_installs,
                        "free": app.free,
                        "contains_ads": app.contains_ads,
                        "offers_iap": app.offers_iap,
                        "last_updated": app.last_updated,
                        "icon": app.icon,
                        "url": app.url,
                    }
                    for app in filtered_apps
                ],
            }

        finally:
            db.close()
