from app.database.database import SessionLocal
from app.database.models import App

from app.services.app_opportunity_service import AppOpportunityService


class AppAnalyzerService:

    def __init__(self):

        self.opportunity_service = AppOpportunityService()

    def analyze_apps(self):

        db = SessionLocal()

        try:

            apps = db.query(App).all()

            results = []

            for app in apps:

                opportunity_score = self.opportunity_service.calculate_score(app)

                results.append(
                    {
                        "app_id": app.app_id,
                        "title": app.title,
                        "developer": app.developer,
                        "score": app.score,
                        "reviews": app.reviews,
                        "installs": app.installs,
                        "real_installs": app.real_installs,
                        "opportunity_score": opportunity_score,
                    }
                )

            results.sort(key=lambda x: x["opportunity_score"], reverse=True)

            return results

        finally:

            db.close()
