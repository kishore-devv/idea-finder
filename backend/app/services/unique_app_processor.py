from app.services.discovery_service import DiscoveryService


class UniqueAppProcessor:

    def __init__(self):
        self.discovery_service = DiscoveryService()

    def process(self, unique_apps):

        processed_apps = []

        for app in unique_apps:

            app_id = app["app_id"]

            print(f"\nProcessing app: {app['title']}")
            print(f"App ID: {app_id}")

            # For now, just collect the app.
            # Database checking will be added next.
            processed_apps.append(
                {"app_id": app_id, "title": app.get("title"), "status": "pending"}
            )

        return processed_apps
