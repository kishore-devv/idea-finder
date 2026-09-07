from fastapi import APIRouter

from app.services.app_analyzer_service import AppAnalyzerService

router = APIRouter(prefix="/analyze", tags=["Analyzer"])


@router.get("/apps")
def analyze_apps():

    service = AppAnalyzerService()

    results = service.analyze_apps()

    return {"total_apps": len(results), "apps": results}
