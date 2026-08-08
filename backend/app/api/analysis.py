from fastapi import APIRouter, HTTPException

from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])


service = AnalysisService()


@router.get("/{app_id}")
def analyze_app(app_id: str):

    result = service.analyze(app_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
