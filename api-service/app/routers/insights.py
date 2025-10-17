from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.ai_insights import AIInsightsService

router = APIRouter(prefix="/insights", tags=["ai-insights"])

ai_insights = AIInsightsService()


class InsightRequest(BaseModel):
    """Request model for AI insights"""
    city_id: int
    city_name: str
    query: str


class InsightResponse(BaseModel):
    """Response model for AI insights"""
    city_id: int
    city_name: str
    query: str
    insight: str


@router.post("/ai", response_model=InsightResponse)
async def get_ai_insight(request: InsightRequest):
    """
    Get AI-powered weather insights using LangGraph.
    Ask natural language questions about weather patterns, trends, and recommendations.
    """
    try:
        insight = await ai_insights.get_insight(
            city_id=request.city_id,
            city_name=request.city_name,
            query=request.query
        )

        return InsightResponse(
            city_id=request.city_id,
            city_name=request.city_name,
            query=request.query,
            insight=insight
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{city_id}", response_model=InsightResponse)
async def get_daily_summary(
    city_id: int,
    city_name: str = Query(..., description="City name for context")
):
    """Get AI-generated daily weather summary for a city"""
    try:
        summary = await ai_insights.generate_daily_summary(
            city_id=city_id,
            city_name=city_name
        )

        return InsightResponse(
            city_id=city_id,
            city_name=city_name,
            query="Daily weather summary",
            insight=summary
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clothing/{city_id}", response_model=InsightResponse)
async def get_clothing_recommendation(
    city_id: int,
    city_name: str = Query(..., description="City name for context")
):
    """Get AI-generated clothing recommendations based on weather"""
    try:
        recommendation = await ai_insights.get_clothing_recommendation(
            city_id=city_id,
            city_name=city_name
        )

        return InsightResponse(
            city_id=city_id,
            city_name=city_name,
            query="Clothing recommendation",
            insight=recommendation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
