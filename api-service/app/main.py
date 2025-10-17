from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import weather, cities, insights, demo

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Weather API Service with AI-powered insights using LangGraph and Pydantic"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(weather.router)
app.include_router(cities.router)
app.include_router(insights.router)
app.include_router(demo.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Weather API Service",
        "version": settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "weather": "/weather",
            "cities": "/cities",
            "insights": "/insights"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
