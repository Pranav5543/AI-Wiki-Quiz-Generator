#!/usr/bin/env python3
"""
Debug test for the AI Wiki Quiz Generator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.wikipedia_scraper import WikipediaScraper
from services.simple_llm_service import SimpleLLMQuizGenerator

def test_wikipedia_scraper():
    """Test Wikipedia scraper"""
    print("Testing Wikipedia scraper...")
    try:
        scraper = WikipediaScraper()
        url = "https://en.wikipedia.org/wiki/Alan_Turing"
        
        print(f"Scraping: {url}")
        article_data = scraper.scrape_article(url)
        
        print("✅ Wikipedia scraper: SUCCESS")
        print(f"   Title: {article_data.get('title', 'Unknown')}")
        print(f"   Summary length: {len(article_data.get('summary', ''))}")
        print(f"   Sections: {len(article_data.get('sections', []))}")
        
        return article_data
        
    except Exception as e:
        print(f"❌ Wikipedia scraper: FAILED")
        print(f"   Error: {str(e)}")
        return None

def test_llm_service():
    """Test LLM service"""
    print("\nTesting LLM service...")
    try:
        llm_service = SimpleLLMQuizGenerator()
        print("✅ LLM service: INITIALIZED")
        
        # Test with simple data
        test_data = {
            'title': 'Test Article',
            'summary': 'This is a test summary.',
            'sections': ['Introduction', 'Main Content'],
            'content_text': 'This is test content for the article.'
        }
        
        print("Generating quiz...")
        quiz_data = llm_service.generate_quiz(test_data)
        
        print("✅ LLM service: SUCCESS")
        print(f"   Questions generated: {len(quiz_data.get('quiz', []))}")
        print(f"   Related topics: {len(quiz_data.get('related_topics', []))}")
        
        return quiz_data
        
    except Exception as e:
        print(f"❌ LLM service: FAILED")
        print(f"   Error: {str(e)}")
        return None

def test_database():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection: SUCCESS")
            return True
    except Exception as e:
        print(f"❌ Database connection: FAILED")
        print(f"   Error: {str(e)}")
        return False

def main():
    """Run debug tests"""
    print("🔍 AI Wiki Quiz Generator - Debug Test")
    print("=" * 50)
    
    # Test database
    db_ok = test_database()
    
    # Test Wikipedia scraper
    article_data = test_wikipedia_scraper()
    
    # Test LLM service
    if article_data:
        quiz_data = test_llm_service()
    else:
        print("\n⚠️  Skipping LLM test due to scraper failure")
        quiz_data = None
    
    print("\n" + "=" * 50)
    print("📊 Debug Results:")
    print(f"   Database: {'✅ OK' if db_ok else '❌ FAILED'}")
    print(f"   Wikipedia Scraper: {'✅ OK' if article_data else '❌ FAILED'}")
    print(f"   LLM Service: {'✅ OK' if quiz_data else '❌ FAILED'}")
    
    if db_ok and article_data and quiz_data:
        print("\n🎉 All components working! The issue might be in the API routing.")
    else:
        print("\n⚠️  Some components failed. Please check the errors above.")

if __name__ == "__main__":
    main()
