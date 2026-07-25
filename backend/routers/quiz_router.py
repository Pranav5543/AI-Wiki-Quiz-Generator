"""
Quiz generation router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional
import logging

from database import get_db, QuizRecord
from services.wikipedia_scraper import WikipediaScraper
from services.simple_llm_service import SimpleLLMQuizGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class QuizRequest(BaseModel):
    """Request model for quiz generation"""
    url: str

class QuizResponse(BaseModel):
    """Response model for quiz generation"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict
    sections: List[str]
    quiz: List[Dict]
    related_topics: List[str]
    created_at: str

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    request: QuizRequest,
    db: Session = Depends(get_db)
):
    """Generate quiz from Wikipedia article URL"""
    try:
        logger.info(f"Generating quiz for URL: {request.url}")
        
        # Check if quiz already exists
        existing_quiz = db.query(QuizRecord).filter(QuizRecord.url == request.url).first()
        if existing_quiz:
            logger.info(f"Quiz already exists for URL: {request.url}")
            return QuizResponse(
                id=existing_quiz.id,
                url=existing_quiz.url,
                title=existing_quiz.title,
                summary=existing_quiz.summary,
                key_entities=existing_quiz.key_entities,
                sections=existing_quiz.sections,
                quiz=existing_quiz.quiz,
                related_topics=existing_quiz.related_topics,
                created_at=existing_quiz.created_at.isoformat()
            )
        
        # Initialize services
        scraper = WikipediaScraper()
        llm_service = SimpleLLMQuizGenerator()
        
        # Scrape Wikipedia article
        logger.info("Scraping Wikipedia article...")
        article_data = scraper.scrape_article(request.url)
        
        # Generate quiz using LLM
        logger.info("Generating quiz with LLM...")
        quiz_data = llm_service.generate_quiz(article_data)
        
        # Create database record
        quiz_record = QuizRecord(
            url=request.url,
            title=article_data['title'],
            summary=article_data['summary'],
            key_entities=article_data['key_entities'],
            sections=article_data['sections'],
            quiz=quiz_data['quiz'],
            related_topics=quiz_data['related_topics'],
            raw_html=article_data['raw_html']
        )
        
        db.add(quiz_record)
        db.commit()
        db.refresh(quiz_record)
        
        logger.info(f"Quiz generated successfully with ID: {quiz_record.id}")
        
        return QuizResponse(
            id=quiz_record.id,
            url=quiz_record.url,
            title=quiz_record.title,
            summary=quiz_record.summary,
            key_entities=quiz_record.key_entities,
            sections=quiz_record.sections,
            quiz=quiz_record.quiz,
            related_topics=quiz_record.related_topics,
            created_at=quiz_record.created_at.isoformat()
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """Get quiz by ID"""
    try:
        quiz_record = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
        if not quiz_record:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        return QuizResponse(
            id=quiz_record.id,
            url=quiz_record.url,
            title=quiz_record.title,
            summary=quiz_record.summary,
            key_entities=quiz_record.key_entities,
            sections=quiz_record.sections,
            quiz=quiz_record.quiz,
            related_topics=quiz_record.related_topics,
            created_at=quiz_record.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quiz")

@router.post("/validate-url")
async def validate_url(request: QuizRequest):
    """Validate Wikipedia URL without generating quiz"""
    try:
        scraper = WikipediaScraper()
        is_valid = scraper.validate_wikipedia_url(request.url)
        
        return {
            "valid": is_valid,
            "message": "Valid Wikipedia URL" if is_valid else "Invalid Wikipedia URL. Please enter a valid Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Article_Name)"
        }
        
    except Exception as e:
        logger.error(f"Error validating URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to validate URL")
