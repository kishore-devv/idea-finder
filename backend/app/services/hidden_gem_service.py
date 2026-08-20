from app.database.database import SessionLocal
from app.database.models import App, Review


class HiddenGemService:

    def get_hidden_gems(
        self,
        min_installs: int = 10000,
        max_installs: int = 1000000,
    ):

        db = SessionLocal()

        try:

            apps = db.query(App).all()

            hidden_gems = []

            for app in apps:

                # Convert installs to integer safely
                installs = self.parse_installs(app.real_installs or app.installs)

                # Skip apps outside our target range
                if installs < min_installs:
                    continue

                if installs > max_installs:
                    continue

                # Get reviews for this app
                reviews = db.query(Review).filter(Review.app_id == app.app_id).all()

                score = self.calculate_hidden_gem_score(app, installs, reviews)

                hidden_gems.append(
                    {
                        "app_id": app.app_id,
                        "title": app.title,
                        "developer": app.developer,
                        "installs": installs,
                        "rating": app.score,
                        "reviews_scraped": len(reviews),
                        "hidden_gem_score": score,
                        "reason": self.generate_reason(app, installs, reviews, score),
                    }
                )

            # Highest opportunity first
            hidden_gems.sort(key=lambda x: x["hidden_gem_score"], reverse=True)

            return hidden_gems

        finally:

            db.close()

    # =====================================================
    # Parse installs
    # =====================================================

    def parse_installs(self, installs):

        if installs is None:
            return 0

        # Already an integer
        if isinstance(installs, int):
            return installs

        # Convert values such as:
        # "10,000+"
        # "100,000+"

        installs = str(installs)

        installs = installs.replace(",", "")
        installs = installs.replace("+", "")

        try:
            return int(installs)

        except ValueError:
            return 0

    # =====================================================
    # Calculate Hidden Gem Score
    # =====================================================

    def calculate_hidden_gem_score(self, app, installs, reviews):

        score = 0

        # ---------------------------------
        # 1. Install Score
        # Smaller but validated apps
        # get more points
        # ---------------------------------

        if 10000 <= installs < 100000:
            score += 30

        elif 100000 <= installs < 500000:
            score += 25

        elif 500000 <= installs <= 1000000:
            score += 15

        # ---------------------------------
        # 2. Rating Score
        # Good ratings prove demand
        # ---------------------------------

        if app.score is not None:

            if app.score >= 4.0:
                score += 25

            elif app.score >= 3.5:
                score += 15

            elif app.score >= 3.0:
                score += 5

        # ---------------------------------
        # 3. Review Opportunity Score
        # Negative reviews indicate
        # problems worth solving
        # ---------------------------------

        total_reviews = len(reviews)

        if total_reviews > 0:

            negative_reviews = 0

            for review in reviews:

                if review.score is not None:

                    if review.score <= 2:
                        negative_reviews += 1

            negative_percentage = (negative_reviews / total_reviews) * 100

            if negative_percentage >= 30:
                score += 30

            elif negative_percentage >= 20:
                score += 20

            elif negative_percentage >= 10:
                score += 10

        # ---------------------------------
        # 4. Review Volume Bonus
        # More reviews = stronger evidence
        # ---------------------------------

        if total_reviews >= 500:
            score += 15

        elif total_reviews >= 100:
            score += 10

        elif total_reviews >= 20:
            score += 5

        # Maximum score = 100

        return min(round(score, 2), 100)

    # =====================================================
    # Generate explanation
    # =====================================================

    def generate_reason(self, app, installs, reviews, score):

        reasons = []

        if 10000 <= installs < 100000:

            reasons.append(
                "The app has relatively low installs but validated market demand."
            )

        elif 100000 <= installs < 1000000:

            reasons.append(
                "The app has proven traction without being an extremely dominant market leader."
            )

        if app.score is not None and app.score >= 4.0:

            reasons.append("A strong rating suggests users value the product.")

        total_reviews = len(reviews)

        if total_reviews > 0:

            negative_reviews = sum(
                1
                for review in reviews
                if review.score is not None and review.score <= 2
            )

            negative_percentage = (negative_reviews / total_reviews) * 100

            if negative_percentage >= 20:

                reasons.append(
                    f"{round(negative_percentage, 1)}% of scraped reviews are negative, suggesting meaningful user problems."
                )

        if not reasons:

            reasons.append(
                "The app matches the selected hidden-gem discovery criteria."
            )

        return " ".join(reasons)


from app.database.database import SessionLocal
from app.database.models import App, Review


class HiddenGemService:

    def get_hidden_gems(
        self,
        min_installs: int = 10000,
        max_installs: int = 1000000,
    ):

        db = SessionLocal()

        try:

            apps = db.query(App).all()

            hidden_gems = []

            for app in apps:

                # Convert installs to integer safely
                installs = self.parse_installs(app.real_installs or app.installs)

                # Skip apps outside our target range
                if installs < min_installs:
                    continue

                if installs > max_installs:
                    continue

                # Get reviews for this app
                reviews = db.query(Review).filter(Review.app_id == app.app_id).all()

                score = self.calculate_hidden_gem_score(app, installs, reviews)

                hidden_gems.append(
                    {
                        "app_id": app.app_id,
                        "title": app.title,
                        "developer": app.developer,
                        "installs": installs,
                        "rating": app.score,
                        "reviews_scraped": len(reviews),
                        "hidden_gem_score": score,
                        "reason": self.generate_reason(app, installs, reviews, score),
                    }
                )

            # Highest opportunity first
            hidden_gems.sort(key=lambda x: x["hidden_gem_score"], reverse=True)

            return hidden_gems

        finally:

            db.close()

    # =====================================================
    # Parse installs
    # =====================================================

    def parse_installs(self, installs):

        if installs is None:
            return 0

        # Already an integer
        if isinstance(installs, int):
            return installs

        # Convert values such as:
        # "10,000+"
        # "100,000+"

        installs = str(installs)

        installs = installs.replace(",", "")
        installs = installs.replace("+", "")

        try:
            return int(installs)

        except ValueError:
            return 0

    # =====================================================
    # Calculate Hidden Gem Score
    # =====================================================

    def calculate_hidden_gem_score(self, app, installs, reviews):

        score = 0

        # ---------------------------------
        # 1. Install Score
        # Smaller but validated apps
        # get more points
        # ---------------------------------

        if 10000 <= installs < 100000:
            score += 30

        elif 100000 <= installs < 500000:
            score += 25

        elif 500000 <= installs <= 1000000:
            score += 15

        # ---------------------------------
        # 2. Rating Score
        # Good ratings prove demand
        # ---------------------------------

        if app.score is not None:

            if app.score >= 4.0:
                score += 25

            elif app.score >= 3.5:
                score += 15

            elif app.score >= 3.0:
                score += 5

        # ---------------------------------
        # 3. Review Opportunity Score
        # Negative reviews indicate
        # problems worth solving
        # ---------------------------------

        total_reviews = len(reviews)

        if total_reviews > 0:

            negative_reviews = 0

            for review in reviews:

                if review.score is not None:

                    if review.score <= 2:
                        negative_reviews += 1

            negative_percentage = (negative_reviews / total_reviews) * 100

            if negative_percentage >= 30:
                score += 30

            elif negative_percentage >= 20:
                score += 20

            elif negative_percentage >= 10:
                score += 10

        # ---------------------------------
        # 4. Review Volume Bonus
        # More reviews = stronger evidence
        # ---------------------------------

        if total_reviews >= 500:
            score += 15

        elif total_reviews >= 100:
            score += 10

        elif total_reviews >= 20:
            score += 5

        # Maximum score = 100

        return min(round(score, 2), 100)

    # =====================================================
    # Generate explanation
    # =====================================================

    def generate_reason(self, app, installs, reviews, score):

        reasons = []

        if 10000 <= installs < 100000:

            reasons.append(
                "The app has relatively low installs but validated market demand."
            )

        elif 100000 <= installs < 1000000:

            reasons.append(
                "The app has proven traction without being an extremely dominant market leader."
            )

        if app.score is not None and app.score >= 4.0:

            reasons.append("A strong rating suggests users value the product.")

        total_reviews = len(reviews)

        if total_reviews > 0:

            negative_reviews = sum(
                1
                for review in reviews
                if review.score is not None and review.score <= 2
            )

            negative_percentage = (negative_reviews / total_reviews) * 100

            if negative_percentage >= 20:

                reasons.append(
                    f"{round(negative_percentage, 1)}% of scraped reviews are negative, suggesting meaningful user problems."
                )

        if not reasons:

            reasons.append(
                "The app matches the selected hidden-gem discovery criteria."
            )

        return " ".join(reasons)
