@echo off
REM AI Wiki Quiz Generator - Windows Deployment Script
REM This script automates the deployment process on Windows

echo 🚀 Starting AI Wiki Quiz Generator Deployment...
echo ==============================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is required but not installed.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is required but not installed.
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is required but not installed.
    exit /b 1
)

echo [SUCCESS] All dependencies are installed.

REM Setup backend
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo [INFO] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Check if .env exists, if not create from example
if not exist ".env" (
    echo [WARNING] .env file not found. Creating from example...
    copy env.example .env
    echo [WARNING] Please edit .env file with your configuration before running the application.
)

cd ..
echo [SUCCESS] Backend setup completed.

REM Setup frontend
echo [INFO] Setting up frontend...
cd frontend

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
npm install

cd ..
echo [SUCCESS] Frontend setup completed.

REM Build for production
echo [INFO] Building for production...
cd frontend
echo [INFO] Building React application...
npm run build
cd ..
echo [SUCCESS] Production build completed.

echo.
echo [SUCCESS] Setup completed successfully!
echo.
echo To start the application:
echo   Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo   Frontend: cd frontend ^&^& npm start
echo.
echo To deploy to Vercel:
echo   vercel --prod
echo.
echo To deploy with Docker:
echo   docker-compose up --build -d
echo.
pause

