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

@router.get("/{app_id}/reviews")
def app_reviews(
    app_id: str, 
    limit: int = 50, 
    offset: int = 0, 
    rating: int = None, 
    search: str = None
):
    return service.get_reviews(app_id, limit, offset, rating, search)
