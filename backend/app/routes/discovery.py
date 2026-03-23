from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from app.services.discovery_service import get_available_industries, get_available_locations, get_industry_roadmap, get_top_growing_startups
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/industries", response_model=List[str])
async def list_industries():
    try:
        return get_available_industries()
    except Exception as e:
        logger.error(f"Error fetching industries: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch industries")

@router.get("/locations", response_model=List[str])
async def list_locations():
    try:
        return get_available_locations()
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch locations")

@router.get("/roadmap", response_model=Dict[str, Any])
async def get_roadmap(industry: str):
    try:
        data = get_industry_roadmap(industry)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except Exception as e:
        logger.error(f"Error fetching roadmap for {industry}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate roadmap")

@router.get("/trending", response_model=List[Dict[str, Any]])
async def get_trending(industry: Optional[str] = None, location: Optional[str] = None):
    try:
        return get_top_growing_startups(industry, location)
    except Exception as e:
        logger.error(f"Error fetching trending startups: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending startups")
