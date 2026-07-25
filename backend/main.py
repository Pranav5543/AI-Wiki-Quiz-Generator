"""
AI Wiki Quiz Generator - FastAPI Backend
Main application entry point

This module contains the FastAPI application configuration and startup logic.
It handles CORS, database initialization, and API routing.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

from database import init_db, get_db
from routers import quiz_router, history_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application.
    Initializes database connection and performs cleanup on shutdown.
    """
    logger.info("Starting AI Wiki Quiz Generator API...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    logger.info("Shutting down AI Wiki Quiz Generator API...")

# Create FastAPI app with enhanced configuration
app = FastAPI(
    title="AI Wiki Quiz Generator API",
    description="""
    ## AI-Powered Quiz Generation Platform
    
    This API generates intelligent quizzes from Wikipedia articles using advanced AI technology.
    
    ### Features:
    - **Smart Quiz Generation**: Uses Google's Gemini AI to create contextual questions
    - **Wikipedia Integration**: Scrapes and processes Wikipedia articles
    - **Interactive Quizzes**: Multiple choice questions with explanations
    - **Quiz History**: Track and manage previously generated quizzes
    - **Real-time Validation**: URL validation and error handling
    
    ### Technology Stack:
    - **Backend**: FastAPI, SQLAlchemy, PostgreSQL
    - **AI**: Google Gemini 2.5 Flash
    - **Web Scraping**: BeautifulSoup4
    - **Frontend**: React, Tailwind CSS
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS with production-ready settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://deepklarity-frontend.onrender.com",  # Add your production domain
        "https://*.onrender.com"  # Allow deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(quiz_router.router, prefix="/api/quiz", tags=["Quiz Generation"])
app.include_router(history_router.router, prefix="/api/history", tags=["Quiz History"])

@app.get("/", response_model=Dict[str, Any])
async def root() -> Dict[str, Any]:
    """
    Root endpoint providing API information.
    
    Returns:
        Dict containing API status and basic information
    """
    return {
        "message": "AI Wiki Quiz Generator API is running!",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        Dict containing health status and system information
    """
    try:
        # Test database connection
        from sqlalchemy import text
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "message": "AI Wiki Quiz Generator API is running!",
            "version": "1.0.0",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "message": "Service temporarily unavailable",
                "error": str(e)
            }
        )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

if __name__ == "__main__":
    # Production-ready configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level="info",
        access_log=True
    )
