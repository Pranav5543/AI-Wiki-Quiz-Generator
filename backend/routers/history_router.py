"""
History router for past quizzes
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional
import logging

from database import get_db, QuizRecord

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class QuizSummary(BaseModel):
    """Summary model for quiz history"""
    id: int
    url: str
    title: str
    summary: str
    created_at: str
    quiz_count: int

class QuizDetail(BaseModel):
    """Detail model for quiz"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: dict
    sections: List[str]
    quiz: List[dict]
    related_topics: List[str]
    created_at: str

@router.get("/", response_model=List[QuizSummary])
async def get_quiz_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get paginated quiz history"""
    try:
        # Calculate offset
        offset = (page - 1) * limit
        
        # Query quizzes with pagination
        quizzes = db.query(QuizRecord).order_by(desc(QuizRecord.created_at)).offset(offset).limit(limit).all()
        
        # Convert to response format
        quiz_summaries = []
        for quiz in quizzes:
            quiz_count = len(quiz.quiz) if quiz.quiz else 0
            quiz_summaries.append(QuizSummary(
                id=quiz.id,
                url=quiz.url,
                title=quiz.title,
                summary=quiz.summary[:200] + "..." if len(quiz.summary) > 200 else quiz.summary,
                created_at=quiz.created_at.isoformat(),
                quiz_count=quiz_count
            ))
        
        logger.info(f"Retrieved {len(quiz_summaries)} quizzes for page {page}")
        return quiz_summaries
        
    except Exception as e:
        logger.error(f"Error retrieving quiz history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quiz history")

@router.get("/{quiz_id}", response_model=QuizDetail)
async def get_quiz_detail(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed quiz information"""
    try:
        quiz_record = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
        if not quiz_record:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        return QuizDetail(
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
        logger.error(f"Error retrieving quiz detail: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quiz detail")

@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """Delete a quiz"""
    try:
        quiz_record = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
        if not quiz_record:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        db.delete(quiz_record)
        db.commit()
        
        logger.info(f"Deleted quiz with ID: {quiz_id}")
        return {"message": "Quiz deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete quiz")

@router.get("/stats/summary")
async def get_stats_summary(db: Session = Depends(get_db)):
    """Get statistics summary"""
    try:
        total_quizzes = db.query(QuizRecord).count()
        
        # Get recent activity (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_quizzes = db.query(QuizRecord).filter(QuizRecord.created_at >= week_ago).count()
        
        return {
            "total_quizzes": total_quizzes,
            "recent_quizzes": recent_quizzes,
            "message": f"Total of {total_quizzes} quizzes generated, {recent_quizzes} in the last week"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")
