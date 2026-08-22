from fastapi import APIRouter

from app.services.market_analysis_service import MarketAnalysisService

router = APIRouter(prefix="/market", tags=["Market Analysis"])


@router.get("/pain-points")
def get_market_pain_points():

    service = MarketAnalysisService()

    results = service.analyze_market()

    return results
