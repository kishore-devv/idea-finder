from datetime import datetime


class AppOpportunityService:

    def calculate_score(self, app):

        score = 0

        # -------------------------
        # Rating score
        # -------------------------

        rating = app.score or 0

        if rating >= 4.5:
            score += 25

        elif rating >= 4.0:
            score += 15

        elif rating >= 3.5:
            score += 5

        # -------------------------
        # Review score
        # -------------------------

        reviews = app.reviews or 0

        if reviews < 1000:
            score += 20

        elif reviews < 10000:
            score += 10

        # -------------------------
        # Install score
        # -------------------------

        installs = app.real_installs or 0

        if 10000 <= installs <= 500000:
            score += 25

        elif 500000 < installs <= 5000000:
            score += 15

        # -------------------------
        # Free app
        # -------------------------

        if app.free:
            score += 5

        # -------------------------
        # In-app purchases
        # -------------------------

        if app.offers_iap:
            score += 5

        return score
