"""
Analytics routes — GET /industry-trends, GET /startups

Returns aggregated analytics and raw startup records from Supabase.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/industry-trends")
async def industry_trends():
    """Return funding distribution and growth trends by industry."""
    # TODO: Phase 6 — wire up data_service
    raise HTTPException(status_code=503, detail="Data service not connected yet. Complete Phase 6.")


@router.get("/startups")
async def list_startups():
    """Return startup records stored in Supabase."""
    # TODO: Phase 6 — wire up data_service
    raise HTTPException(status_code=503, detail="Data service not connected yet. Complete Phase 6.")
