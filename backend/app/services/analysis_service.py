from app.database.database import SessionLocal
from app.database.models import App, Review


class AnalysisService:

    def analyze(self, app_id: str):

        db = SessionLocal()

        try:

            # -----------------------------
            # Get app
            # -----------------------------

            app = db.query(App).filter(App.app_id == app_id).first()

            if not app:
                from app.services.unique_app_processor import UniqueAppProcessor
                processor = UniqueAppProcessor()
                processor.process([{"app_id": app_id}])
                
                # Fetch again
                app = db.query(App).filter(App.app_id == app_id).first()
                if not app:
                    return {"error": "App not found"}

            # -----------------------------
            # Get reviews
            # -----------------------------

            reviews = db.query(Review).filter(Review.app_id == app_id).all()

            # -----------------------------
            # Basic statistics
            # -----------------------------

            total_reviews = len(reviews)

            positive = 0
            neutral = 0
            negative = 0

            for review in reviews:

                if review.score is None:
                    continue

                if review.score >= 4:
                    positive += 1

                elif review.score == 3:
                    neutral += 1

                elif review.score <= 2:
                    negative += 1

            # -----------------------------
            # Extract pain points
            # -----------------------------

            pain_points = self.extract_pain_points(reviews)

            # -----------------------------
            # Calculate pain-point percentages
            # -----------------------------

            pain_point_percentages = {}

            if total_reviews > 0:

                for category, count in pain_points.items():

                    percentage = (count / total_reviews) * 100

                    pain_point_percentages[category] = round(percentage, 2)

            else:

                for category in pain_points:
                    pain_point_percentages[category] = 0

            # -----------------------------
            # Rank pain points
            # -----------------------------

            top_pain_points = self.get_top_pain_points(
                pain_points, pain_point_percentages
            )

            # -----------------------------
            # Calculate opportunity scores
            # -----------------------------

            opportunity_scores = self.calculate_opportunity_scores(
                pain_points, pain_point_percentages
            )

            # -----------------------------
            # Generate startup opportunities
            # -----------------------------

            opportunities = self.generate_opportunities(
                opportunity_scores, pain_points, pain_point_percentages
            )

            # -----------------------------
            # Return analysis
            # -----------------------------

            return {
                "app": {
                    "app_id": app.app_id,
                    "title": app.title,
                    "developer": app.developer,
                    "score": app.score,
                    "ratings": app.ratings,
                    "reviews": app.reviews,
                },
                "review_analysis": {
                    "total_reviews": total_reviews,
                    "positive": positive,
                    "neutral": neutral,
                    "negative": negative,
                },
                "pain_points": pain_points,
                "pain_point_percentages": pain_point_percentages,
                "top_pain_points": top_pain_points,
                "opportunity_scores": opportunity_scores,
                "opportunities": opportunities,
            }

        finally:

            db.close()

    def get_reviews(self, app_id: str, limit: int = 50, offset: int = 0, rating: int = None, search: str = None):
        db = SessionLocal()
        try:
            # Check if app exists
            app = db.query(App).filter(App.app_id == app_id).first()
            if not app:
                from app.services.unique_app_processor import UniqueAppProcessor
                processor = UniqueAppProcessor()
                processor.process([{"app_id": app_id}])
                
            query = db.query(Review).filter(Review.app_id == app_id)
            
            if rating is not None:
                query = query.filter(Review.score == rating)
                
            if search:
                query = query.filter(Review.text.ilike(f"%{search}%"))
                
            total = query.count()
            reviews = query.offset(offset).limit(limit).all()
            return {
                "total": total,
                "limit": limit,
                "offset": offset,
                "reviews": [
                    {
                        "review_id": r.review_id,
                        "text": r.text,
                        "score": r.score,
                        "thumbs_up": getattr(r, 'thumbs_up', 0),
                        "date": getattr(r, 'date', None)
                    } for r in reviews
                ]
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

            # -----------------------------
            # Pricing
            # -----------------------------

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

            # -----------------------------
            # Billing
            # -----------------------------

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

            # -----------------------------
            # Payment
            # -----------------------------

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

            # -----------------------------
            # Errors
            # -----------------------------

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

            # -----------------------------
            # Usability
            # -----------------------------

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

    # =====================================================
    # Calculate Opportunity Scores
    # =====================================================

    def calculate_opportunity_scores(self, pain_points, pain_point_percentages):

        severity_weights = {
            "pricing": 1.0,
            "billing": 1.2,
            "payment": 1.3,
            "errors": 1.5,
            "usability": 1.1,
        }

        opportunity_scores = {}

        for category, percentage in pain_point_percentages.items():

            severity = severity_weights.get(category, 1.0)

            score = percentage * severity

            opportunity_scores[category] = round(score, 2)

        return opportunity_scores

    # =====================================================
    # Rank Pain Points
    # =====================================================

    def get_top_pain_points(self, pain_points, pain_point_percentages):

        ranked = []

        for category, count in pain_points.items():

            ranked.append(
                {
                    "category": category,
                    "count": count,
                    "percentage": pain_point_percentages.get(category, 0),
                }
            )

        # Highest number of mentions first

        ranked.sort(key=lambda x: x["count"], reverse=True)

        return ranked

    # =====================================================
    # Generate Startup Opportunities
    # =====================================================

    def generate_opportunities(
        self, opportunity_scores, pain_points, pain_point_percentages
    ):

        opportunity_templates = {
            "pricing": {
                "opportunity": "Build an affordable alternative with transparent pricing.",
                "target_users": "Freelancers, small businesses, and price-sensitive users.",
                "problem": "Users complain about expensive pricing, costs, or subscriptions.",
            },
            "billing": {
                "opportunity": "Build a simple billing platform with transparent charges and easier refunds.",
                "target_users": "Small businesses, freelancers, and online sellers.",
                "problem": "Users experience billing confusion, unexpected charges, duplicate charges, or refund problems.",
            },
            "payment": {
                "opportunity": "Build a simpler payment solution with reliable and flexible payment options.",
                "target_users": "Small businesses, freelancers, and online merchants.",
                "problem": "Users experience problems with payments or limited payment methods.",
            },
            "errors": {
                "opportunity": "Build a more reliable product focused on stability, error prevention, and recovery.",
                "target_users": "Businesses and professionals who depend on reliable software.",
                "problem": "Users report bugs, crashes, broken features, or inaccessible functionality.",
            },
            "usability": {
                "opportunity": "Build a simpler and more intuitive alternative focused on ease of use.",
                "target_users": "Beginners, freelancers, and small business owners.",
                "problem": "Users find the existing product difficult, confusing, or complicated to use.",
            },
        }

        opportunities = []

        # -----------------------------
        # Sort categories by opportunity
        # score, highest first
        # -----------------------------

        ranked_categories = sorted(
            opportunity_scores.items(), key=lambda item: item[1], reverse=True
        )

        # -----------------------------
        # Generate opportunities
        # -----------------------------

        for category, score in ranked_categories:

            count = pain_points.get(category, 0)

            percentage = pain_point_percentages.get(category, 0)

            template = opportunity_templates.get(category)

            if not template:
                continue

            # -----------------------------
            # Skip categories with
            # zero mentions
            # -----------------------------

            if count == 0:
                continue

            opportunities.append(
                {
                    "category": category,
                    "opportunity_score": score,
                    "pain_point_count": count,
                    "pain_point_percentage": percentage,
                    "opportunity": template["opportunity"],
                    "target_users": template["target_users"],
                    "problem": template["problem"],
                }
            )

        return opportunities
