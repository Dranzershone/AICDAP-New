#!/bin/bash

# AICDAP Backend Startup Script
# This script ensures the backend starts with the proper virtual environment

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AICDAP Backend...${NC}"

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo -e "${RED}Error: Please run this script from the AICDAP project root directory${NC}"
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found. Please create it first:${NC}"
    echo "  cd backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Check if requirements are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
source venv/bin/activate

# Check for critical dependencies
python -c "import torch, torch_geometric, fastapi, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing missing dependencies...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Check if data directory exists
if [ ! -d "../data_r3.2/processed" ]; then
    echo -e "${YELLOW}Warning: Data directory not found at ../data_r3.2/processed${NC}"
    echo -e "${YELLOW}The system will use mock data for demonstration${NC}"
fi

# Check if answer files exist
if [ ! -d "../answers" ]; then
    echo -e "${YELLOW}Warning: Answer directory not found at ../answers${NC}"
    echo -e "${YELLOW}Creating answer directory with sample data...${NC}"
    mkdir -p ../answers
fi

# Set environment variables if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Kill any existing backend process
echo -e "${YELLOW}Checking for existing backend processes...${NC}"
pkill -f "python.*main.py" 2>/dev/null || true

# Start the backend
echo -e "${GREEN}Starting FastAPI backend server...${NC}"
echo -e "${YELLOW}Backend will be available at: http://localhost:8000${NC}"
echo -e "${YELLOW}Health check endpoint: http://localhost:8000/health${NC}"
echo -e "${YELLOW}Insider threat endpoint: http://localhost:8000/api/insider-threat/analyze${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start with proper logging
python main.py

# Cleanup on exit
trap 'echo -e "\n${YELLOW}Shutting down backend server...${NC}"; exit 0' INT TERM
