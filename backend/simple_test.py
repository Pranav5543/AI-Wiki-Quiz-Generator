#!/usr/bin/env python3
"""
Simple test for the AI Wiki Quiz Generator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from services.wikipedia_scraper import WikipediaScraper
        print("✅ WikipediaScraper: OK")
        
        from services.simple_llm_service import SimpleLLMQuizGenerator
        print("✅ SimpleLLMQuizGenerator: OK")
        
        from database import engine
        print("✅ Database engine: OK")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_database():
    """Test database connection"""
    print("\nTesting database...")
    try:
        from database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database: OK")
            return True
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False

def test_scraper():
    """Test Wikipedia scraper"""
    print("\nTesting Wikipedia scraper...")
    try:
        from services.wikipedia_scraper import WikipediaScraper
        scraper = WikipediaScraper()
        url = "https://en.wikipedia.org/wiki/Alan_Turing"
        article_data = scraper.scrape_article(url)
        print(f"✅ Scraper: OK - Title: {article_data.get('title', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Scraper error: {str(e)}")
        return False

def test_llm():
    """Test LLM service"""
    print("\nTesting LLM service...")
    try:
        from services.simple_llm_service import SimpleLLMQuizGenerator
        llm = SimpleLLMQuizGenerator()
        print("✅ LLM service: OK")
        return True
    except Exception as e:
        print(f"❌ LLM error: {str(e)}")
        return False

def main():
    """Run tests"""
    print("AI Wiki Quiz Generator - Simple Test")
    print("=" * 40)
    
    imports_ok = test_imports()
    db_ok = test_database()
    scraper_ok = test_scraper()
    llm_ok = test_llm()
    
    print("\n" + "=" * 40)
    print("Results:")
    print(f"Imports: {'OK' if imports_ok else 'FAILED'}")
    print(f"Database: {'OK' if db_ok else 'FAILED'}")
    print(f"Scraper: {'OK' if scraper_ok else 'FAILED'}")
    print(f"LLM: {'OK' if llm_ok else 'FAILED'}")

if __name__ == "__main__":
    main()
