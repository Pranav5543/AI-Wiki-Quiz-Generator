"""
Configuration settings for the AI Wiki Quiz Generator
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_URL = "postgresql://neondb_owner:npg_6EzKLejbWD1m@ep-shiny-sea-ahppzxgs-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyCnwA4P2SWoIQA28BbRrKgXoQQpOcnIm08"

# Application Configuration
DEBUG = True
LOG_LEVEL = "INFO"
HOST = "0.0.0.0"
PORT = 8000
WORKERS = 1
RELOAD = True

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001"
]
