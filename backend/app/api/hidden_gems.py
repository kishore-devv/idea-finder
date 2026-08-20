from fastapi import APIRouter, Query

from app.services.hidden_gem_service import HiddenGemService

router = APIRouter(prefix="/discover", tags=["Hidden Gems"])


@router.get("/hidden-gems")
def get_hidden_gems(
    min_installs: int = Query(10000, ge=0),
    max_installs: int = Query(1000000, ge=1),
):

    service = HiddenGemService()

    results = service.get_hidden_gems(
        min_installs=min_installs,
        max_installs=max_installs,
    )

    return {
        "count": len(results),
        "hidden_gems": results,
    }
