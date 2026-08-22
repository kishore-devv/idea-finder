from app.database.database import SessionLocal
from app.database.models import App, Review


class MarketAnalysisService:

    # =====================================================
    # Main Market Analysis
    # =====================================================

    def analyze_market(self):

        db = SessionLocal()

        try:

            apps = db.query(App).all()

            # Store market-wide statistics
            market_pain_points = {
                "pricing": {
                    "apps_affected": 0,
                    "total_mentions": 0,
                    "total_percentage": 0,
                    "apps": [],
                },
                "billing": {
                    "apps_affected": 0,
                    "total_mentions": 0,
                    "total_percentage": 0,
                    "apps": [],
                },
                "payment": {
                    "apps_affected": 0,
                    "total_mentions": 0,
                    "total_percentage": 0,
                    "apps": [],
                },
                "errors": {
                    "apps_affected": 0,
                    "total_mentions": 0,
                    "total_percentage": 0,
                    "apps": [],
                },
                "usability": {
                    "apps_affected": 0,
                    "total_mentions": 0,
                    "total_percentage": 0,
                    "apps": [],
                },
            }

            total_apps_analyzed = 0

            # ---------------------------------------------
            # Analyze each app
            # ---------------------------------------------

            for app in apps:

                reviews = db.query(Review).filter(Review.app_id == app.app_id).all()

                total_reviews = len(reviews)

                # Skip apps with no scraped reviews
                if total_reviews == 0:
                    continue

                total_apps_analyzed += 1

                pain_points = self.extract_pain_points(reviews)

                # -----------------------------------------
                # Add app results to market statistics
                # -----------------------------------------

                for category, count in pain_points.items():

                    if count == 0:
                        continue

                    percentage = round((count / total_reviews) * 100, 2)

                    market_pain_points[category]["apps_affected"] += 1

                    market_pain_points[category]["total_mentions"] += count

                    market_pain_points[category]["total_percentage"] += percentage

                    market_pain_points[category]["apps"].append(
                        {
                            "app_id": app.app_id,
                            "title": app.title,
                            "mentions": count,
                            "percentage": percentage,
                            "reviews_analyzed": total_reviews,
                        }
                    )

            # ---------------------------------------------
            # Calculate average percentage
            # ---------------------------------------------

            results = []

            for category, data in market_pain_points.items():

                apps_affected = data["apps_affected"]

                if apps_affected > 0:

                    average_percentage = round(
                        data["total_percentage"] / apps_affected, 2
                    )

                else:

                    average_percentage = 0

                # Sort affected apps by mentions
                data["apps"].sort(key=lambda x: x["mentions"], reverse=True)

                results.append(
                    {
                        "category": category,
                        "apps_affected": apps_affected,
                        "total_mentions": data["total_mentions"],
                        "average_percentage": average_percentage,
                        "apps": data["apps"],
                    }
                )

            # ---------------------------------------------
            # Rank market pain points
            # ---------------------------------------------

            results.sort(
                key=lambda x: (
                    x["apps_affected"],
                    x["total_mentions"],
                    x["average_percentage"],
                ),
                reverse=True,
            )

            return {
                "total_apps_analyzed": total_apps_analyzed,
                "market_pain_points": results,
            }

        finally:

            db.close()

    # =====================================================
    # Extract Pain Points
    # =====================================================

    def extract_pain_points(self, reviews):

        pain_points = {
            "pricing": 0,
            "billing": 0,
            "payment": 0,
            "errors": 0,
            "usability": 0,
        }

        for review in reviews:

            text = (review.text or "").lower()

            # Pricing
            if any(
                word in text
                for word in [
                    "price",
                    "pricing",
                    "expensive",
                    "cost",
                    "increase",
                    "subscription",
                ]
            ):
                pain_points["pricing"] += 1

            # Billing
            if any(
                word in text
                for word in [
                    "charge",
                    "charged",
                    "billing",
                    "bill",
                    "refund",
                    "double",
                ]
            ):
                pain_points["billing"] += 1

            # Payment
            if any(
                word in text
                for word in [
                    "payment",
                    "apple pay",
                    "paypal",
                    "stripe",
                ]
            ):
                pain_points["payment"] += 1

            # Errors
            if any(
                word in text
                for word in [
                    "error",
                    "bug",
                    "crash",
                    "broken",
                    "inaccessible",
                ]
            ):
                pain_points["errors"] += 1

            # Usability
            if any(
                word in text
                for word in [
                    "difficult",
                    "confusing",
                    "hard to use",
                    "complicated",
                ]
            ):
                pain_points["usability"] += 1

        return pain_points
