#!/bin/bash

# AI Wiki Quiz Generator - Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting AI Wiki Quiz Generator Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not installed."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed."
        exit 1
    fi
    
    print_success "All dependencies are installed."
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Check if .env exists, if not create from example
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from example..."
        cp env.example .env
        print_warning "Please edit .env file with your configuration before running the application."
    fi
    
    cd ..
    print_success "Backend setup completed."
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
    print_success "Frontend setup completed."
}

# Build for production
build_production() {
    print_status "Building for production..."
    
    # Build frontend
    cd frontend
    print_status "Building React application..."
    npm run build
    cd ..
    
    print_success "Production build completed."
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    cd backend
    source venv/bin/activate
    if [ -d "tests" ]; then
        print_status "Running backend tests..."
        python -m pytest tests/ -v
    else
        print_warning "No backend tests found."
    fi
    cd ..
    
    # Frontend tests
    cd frontend
    print_status "Running frontend tests..."
    npm test -- --watchAll=false
    cd ..
    
    print_success "All tests completed."
}

# Deploy to Vercel
deploy_vercel() {
    print_status "Deploying to Vercel..."
    
    if ! command -v vercel &> /dev/null; then
        print_status "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    vercel --prod
    
    print_success "Deployment to Vercel completed."
}

# Deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is required but not installed."
        exit 1
    fi
    
    docker-compose up --build -d
    
    print_success "Docker deployment completed."
}

# Main deployment function
main() {
    echo "🧠 AI Wiki Quiz Generator - Deployment Script"
    echo "=============================================="
    
    # Parse command line arguments
    case "${1:-setup}" in
        "setup")
            check_dependencies
            setup_backend
            setup_frontend
            print_success "Setup completed successfully!"
            print_status "To start the application:"
            print_status "  Backend:  cd backend && source venv/bin/activate && python main.py"
            print_status "  Frontend: cd frontend && npm start"
            ;;
        "build")
            build_production
            ;;
        "test")
            run_tests
            ;;
        "deploy-vercel")
            build_production
            deploy_vercel
            ;;
        "deploy-docker")
            deploy_docker
            ;;
        "full")
            check_dependencies
            setup_backend
            setup_frontend
            build_production
            run_tests
            deploy_vercel
            ;;
        *)
            echo "Usage: $0 {setup|build|test|deploy-vercel|deploy-docker|full}"
            echo ""
            echo "Commands:"
            echo "  setup          - Setup development environment"
            echo "  build          - Build for production"
            echo "  test           - Run all tests"
            echo "  deploy-vercel  - Deploy to Vercel"
            echo "  deploy-docker  - Deploy with Docker"
            echo "  full           - Complete setup and deployment"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"

