#!/usr/bin/env python3
"""
Test script to verify the AI Wiki Quiz Generator application
"""

import requests
import time
import json

def test_backend():
    """Test backend endpoints"""
    print("🧪 Testing Backend API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Backend health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend health check: FAILED ({response.status_code})")
            return False
            
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Backend root endpoint: PASSED")
        else:
            print(f"❌ Backend root endpoint: FAILED ({response.status_code})")
            
        # Test API documentation
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API documentation: ACCESSIBLE")
        else:
            print(f"❌ API documentation: NOT ACCESSIBLE ({response.status_code})")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend connection: FAILED - Backend not running")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {str(e)}")
        return False

def test_quiz_generation():
    """Test quiz generation with a sample URL"""
    print("\n🧪 Testing Quiz Generation...")
    
    base_url = "http://localhost:8000"
    test_url = "https://en.wikipedia.org/wiki/Alan_Turing"
    
    try:
        # Test URL validation
        print("   Testing URL validation...")
        response = requests.post(
            f"{base_url}/api/quiz/validate-url",
            json={"url": test_url}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("valid"):
                print("✅ URL validation: PASSED")
            else:
                print("❌ URL validation: FAILED - Invalid URL")
                return False
        else:
            print(f"❌ URL validation: FAILED ({response.status_code})")
            return False
            
        # Test quiz generation
        print("   Testing quiz generation...")
        response = requests.post(
            f"{base_url}/api/quiz/generate",
            json={"url": test_url}
        )
        
        if response.status_code == 200:
            quiz_data = response.json()
            print("✅ Quiz generation: PASSED")
            print(f"   Generated quiz for: {quiz_data.get('title', 'Unknown')}")
            print(f"   Number of questions: {len(quiz_data.get('quiz', []))}")
            print(f"   Related topics: {len(quiz_data.get('related_topics', []))}")
            return True
        else:
            print(f"❌ Quiz generation: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Quiz generation test error: {str(e)}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    print("\n🧪 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: ACCESSIBLE")
            return True
        else:
            print(f"❌ Frontend: NOT ACCESSIBLE ({response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend: NOT RUNNING")
        return False
    except Exception as e:
        print(f"❌ Frontend test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Wiki Quiz Generator - Application Test")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend()
    
    if backend_ok:
        # Test quiz generation
        quiz_ok = test_quiz_generation()
        
        # Test frontend
        frontend_ok = test_frontend()
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print(f"   Backend API: {'✅ PASSED' if backend_ok else '❌ FAILED'}")
        print(f"   Quiz Generation: {'✅ PASSED' if quiz_ok else '❌ FAILED'}")
        print(f"   Frontend: {'✅ PASSED' if frontend_ok else '❌ FAILED'}")
        
        if backend_ok and quiz_ok and frontend_ok:
            print("\n🎉 All tests passed! Application is ready to use.")
            print("\n🌐 Access URLs:")
            print("   Frontend: http://localhost:3000")
            print("   Backend API: http://localhost:8000")
            print("   API Documentation: http://localhost:8000/docs")
        else:
            print("\n⚠️  Some tests failed. Please check the issues above.")
    else:
        print("\n❌ Backend is not running. Please start the backend first.")
        print("   Run: cd backend && python main.py")

if __name__ == "__main__":
    main()
