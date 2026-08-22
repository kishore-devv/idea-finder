class AppProcessingService:

    def __init__(self, review_service, analysis_service, app_repository):
        self.review_service = review_service
        self.analysis_service = analysis_service
        self.app_repository = app_repository

    def process_apps(self, apps):

        processed_apps = []

        for app in apps:

            app_id = app["app_id"]

            print(f"\nProcessing app: {app['title']}")
            print(f"App ID: {app_id}")

            # 1. Save or update app
            saved_app = self.app_repository.upsert_app(app)

            # 2. Scrape reviews once
            reviews = self.review_service.get_reviews(app_id=app_id)

            # 3. Analyze reviews
            analysis = self.analysis_service.analyze(reviews=reviews)

            # 4. Save analysis
            self.app_repository.save_analysis(app_id=app_id, analysis=analysis)

            processed_apps.append(
                {
                    "app_id": app_id,
                    "title": app["title"],
                    "reviews_processed": len(reviews),
                    "analysis": analysis,
                }
            )

        return {"apps_processed": len(processed_apps), "apps": processed_apps}
