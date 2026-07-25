#!/usr/bin/env python3
"""
Simple backend server without database dependencies
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import json

app = FastAPI(title="Simple Quiz Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def validate_wikipedia_url(url: str) -> bool:
    """Validate if URL is a Wikipedia article"""
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        is_wikipedia = (
            netloc == 'en.wikipedia.org' or 
            netloc == 'www.en.wikipedia.org' or
            netloc.endswith('.wikipedia.org')
        )
        is_wiki_article = '/wiki/' in parsed.path
        is_not_special = not any(skip in url for skip in [
            'Special:', 'Talk:', 'User:', 'File:', 'Category:', 
            'Template:', 'Help:', 'Portal:', 'Wikipedia:'
        ])
        return is_wikipedia and is_wiki_article and is_not_special
    except:
        return False

def scrape_wikipedia_article(url: str):
    """Scrape Wikipedia article content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', {'class': 'firstHeading'})
        title = title_elem.get_text().strip() if title_elem else "Unknown Title"
        
        # Extract summary
        content_div = soup.find('div', {'id': 'mw-content-text'})
        summary = "No summary available"
        if content_div:
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 100:
                    summary = text[:500] + "..." if len(text) > 500 else text
                    break
        
        # Extract content text
        content_text = ""
        if content_div:
            for element in content_div.find_all(['table', 'div', 'span'], {'class': ['navbox', 'infobox', 'reference']}):
                element.decompose()
            text = content_div.get_text()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\[edit\]', '', text)
            content_text = text.strip()[:8000]
        
        return {
            'url': url,
            'title': title,
            'summary': summary,
            'content_text': content_text
        }
    except Exception as e:
        raise Exception(f"Failed to scrape Wikipedia article: {str(e)}")

def generate_simple_quiz(article_data):
    """Generate a simple quiz from article data"""
    title = article_data['title']
    content = article_data['content_text']
    
    # Simple quiz generation based on content
    questions = []
    
    # Question 1: About the main topic
    questions.append({
        "id": 1,
        "question": f"What is the main topic of the Wikipedia article '{title}'?",
        "options": [
            title,
            "A related topic",
            "Something else",
            "Not specified"
        ],
        "correct_answer": 0,
        "explanation": f"The article is about {title}."
    })
    
    # Question 2: About the content
    if len(content) > 100:
        questions.append({
            "id": 2,
            "question": f"Based on the article about {title}, which statement is most likely true?",
            "options": [
                f"The article provides detailed information about {title}",
                "The article is very short",
                "The article has no content",
                "The article is about something else"
            ],
            "correct_answer": 0,
            "explanation": f"The article contains detailed information about {title}."
        })
    
    # Question 3: About Wikipedia
    questions.append({
        "id": 3,
        "question": "What type of source is this article?",
        "options": [
            "Wikipedia article",
            "News article",
            "Blog post",
            "Academic paper"
        ],
        "correct_answer": 0,
        "explanation": "This is a Wikipedia article, which is an online encyclopedia."
    })
    
    return {
        "quiz": questions,
        "related_topics": [title, "Wikipedia", "Online encyclopedia"]
    }

@app.get("/")
async def root():
    return {"message": "Simple Quiz Generator API is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API is running"}

@app.options("/api/quiz/validate-url")
async def options_validate_url():
    return {"message": "OK"}

@app.options("/api/quiz/generate")
async def options_generate():
    return {"message": "OK"}

@app.post("/api/quiz/validate-url")
async def validate_url(request: dict):
    """Validate Wikipedia URL"""
    url = request.get('url', '')
    is_valid = validate_wikipedia_url(url)
    
    return {
        "valid": is_valid,
        "message": "Valid Wikipedia URL" if is_valid else "Invalid Wikipedia URL. Please enter a valid Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Article_Name)"
    }

@app.post("/api/quiz/generate")
async def generate_quiz(request: dict):
    """Generate quiz from Wikipedia URL"""
    url = request.get('url', '')
    
    # Validate URL
    if not validate_wikipedia_url(url):
        raise HTTPException(status_code=400, detail="Invalid Wikipedia URL")
    
    try:
        # Scrape article
        article_data = scrape_wikipedia_article(url)
        
        # Generate quiz
        quiz_data = generate_simple_quiz(article_data)
        
        return {
            "id": 1,
            "url": url,
            "title": article_data['title'],
            "summary": article_data['summary'],
            "quiz": quiz_data['quiz'],
            "related_topics": quiz_data['related_topics'],
            "created_at": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

if __name__ == "__main__":
    print("Starting Simple Quiz Generator API...")
    print("Backend will be available at: http://localhost:8000")
    print("API docs will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
