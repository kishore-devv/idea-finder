from datetime import datetime, timedelta


class AppFilterService:
    """
    Centralized filtering logic for Google Play apps.

    Can filter both:
    - SQLAlchemy App database objects
    - Raw Google Play app dictionaries

    The same rules are therefore reusable by discovery and exploration.
    """

    INSTALL_BUCKETS = {
        "0-1k": (0, 1_000),
        "1k-5k": (1_000, 5_000),
        "5k-10k": (5_000, 10_000),
        "10k-20k": (10_000, 20_000),
        "20k-50k": (20_000, 50_000),
        "50k-100k": (50_000, 100_000),
        "100k-200k": (100_000, 200_000),
        "200k-300k": (200_000, 300_000),
        "300k-500k": (300_000, 500_000),
        "500k-1m": (500_000, 1_000_000),
        "1m-2m": (1_000_000, 2_000_000),
        "2m-5m": (2_000_000, 5_000_000),
        "5m-10m": (5_000_000, 10_000_000),
        "10m-20m": (10_000_000, 20_000_000),
        "20m-50m": (20_000_000, 50_000_000),
        "50m-100m": (50_000_000, 100_000_000),
        "100m+": (100_000_000, None),
    }

    @staticmethod
    def get_value(app, field, default=None):
        """
        Works with both:
        - SQLAlchemy objects
        - dictionaries
        """

        if isinstance(app, dict):
            return app.get(field, default)

        return getattr(app, field, default)

    @classmethod
    def matches(
        cls,
        app,
        category=None,
        keyword=None,
        min_rating=None,
        max_rating=None,
        min_ratings=None,
        max_ratings=None,
        min_reviews=None,
        max_reviews=None,
        min_installs=None,
        max_installs=None,
        install_bucket=None,
        free=None,
        contains_ads=None,
        offers_iap=None,
        developer=None,
        recently_updated_days=None,
        old_not_updated_days=None,
    ):
        """
        Return True when an app satisfies every supplied filter.
        """

        # ---------------------------------------------------------
        # Category
        # ---------------------------------------------------------

        if category:
            app_category = cls.get_value(app, "category")

            if not app_category:
                return False

            if category.lower() not in app_category.lower():
                return False

        # ---------------------------------------------------------
        # Keyword
        # ---------------------------------------------------------

        if keyword:
            keyword = keyword.lower().strip()

            searchable_text = " ".join(
                [
                    str(cls.get_value(app, "title") or ""),
                    str(cls.get_value(app, "description") or ""),
                    str(cls.get_value(app, "developer") or ""),
                ]
            ).lower()

            if keyword not in searchable_text:
                return False

        # ---------------------------------------------------------
        # Rating
        # ---------------------------------------------------------

        score = cls.get_value(app, "score")

        if min_rating is not None:
            if score is None or score < min_rating:
                return False

        if max_rating is not None:
            if score is None or score > max_rating:
                return False

        # ---------------------------------------------------------
        # Number of ratings
        # ---------------------------------------------------------

        ratings = cls.get_value(app, "ratings")

        if min_ratings is not None:
            if ratings is None or ratings < min_ratings:
                return False

        if max_ratings is not None:
            if ratings is None or ratings > max_ratings:
                return False

        # ---------------------------------------------------------
        # Number of reviews
        # ---------------------------------------------------------

        reviews = cls.get_value(app, "reviews")

        if min_reviews is not None:
            if reviews is None or reviews < min_reviews:
                return False

        if max_reviews is not None:
            if reviews is None or reviews > max_reviews:
                return False

        # ---------------------------------------------------------
        # Installs
        # ---------------------------------------------------------

        real_installs = cls.get_value(app, "real_installs")

        if min_installs is not None:
            if real_installs is None or real_installs < min_installs:
                return False

        if max_installs is not None:
            if real_installs is None or real_installs > max_installs:
                return False

        # ---------------------------------------------------------
        # Install bucket
        # ---------------------------------------------------------

        if install_bucket:

            normalized_bucket = install_bucket.lower().strip()

            bucket = cls.INSTALL_BUCKETS.get(normalized_bucket)

            if bucket is None:
                return False

            min_bucket, max_bucket = bucket

            if real_installs is None:
                return False

            if real_installs < min_bucket:
                return False

            if max_bucket is not None and real_installs >= max_bucket:
                return False

        # ---------------------------------------------------------
        # Free / Paid
        # ---------------------------------------------------------

        if free is not None:

            app_free = cls.get_value(app, "free")

            if app_free != free:
                return False

        # ---------------------------------------------------------
        # Contains Ads
        # ---------------------------------------------------------

        if contains_ads is not None:

            app_contains_ads = cls.get_value(
                app,
                "contains_ads",
            )

            if app_contains_ads != contains_ads:
                return False

        # ---------------------------------------------------------
        # In-App Purchases
        # ---------------------------------------------------------

        if offers_iap is not None:

            app_offers_iap = cls.get_value(
                app,
                "offers_iap",
            )

            if app_offers_iap != offers_iap:
                return False

        # ---------------------------------------------------------
        # Developer
        # ---------------------------------------------------------

        if developer:

            app_developer = cls.get_value(
                app,
                "developer",
            )

            if not app_developer:
                return False

            if developer.lower() not in app_developer.lower():
                return False

        # ---------------------------------------------------------
        # Last Updated
        # ---------------------------------------------------------

        last_updated = cls.get_value(
            app,
            "last_updated",
        )

        if recently_updated_days is not None:

            if not last_updated:
                return False

            updated_date = cls.parse_date(last_updated)

            if updated_date is None:
                return False

            cutoff = datetime.utcnow() - timedelta(days=recently_updated_days)

            if updated_date < cutoff:
                return False

        # ---------------------------------------------------------
        # Old / Not Updated
        # ---------------------------------------------------------

        if old_not_updated_days is not None:

            if not last_updated:
                return False

            updated_date = cls.parse_date(last_updated)

            if updated_date is None:
                return False

            cutoff = datetime.utcnow() - timedelta(days=old_not_updated_days)

            if updated_date >= cutoff:
                return False

        return True

    @staticmethod
    def parse_date(value):
        """
        Parse common Google Play date formats.
        """

        if not value:
            return None

        if isinstance(value, datetime):
            return value

        value = str(value)

        formats = [
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        ]

        for date_format in formats:

            try:
                return datetime.strptime(
                    value,
                    date_format,
                )
            except ValueError:
                continue

        try:
            return datetime.fromisoformat(value)

        except ValueError:
            return None

    @classmethod
    def filter_apps(cls, apps, **filters):
        """
        Filter a list of apps using the same rules as matches().
        """

        return [app for app in apps if cls.matches(app, **filters)]
