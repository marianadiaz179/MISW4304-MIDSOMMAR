#!/bin/bash

# Newman Test Runner for Blacklist Microservice
# Universidad de los Andes - MISW4304

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COLLECTION_FILE="Blacklist_Microservice_With_Tests.postman_collection.json"
ENVIRONMENT_FILE=""
BASE_URL="http://localhost:3000"
SECRET_TOKEN="test_secret_token_123"
REPORT_DIR="newman_reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create reports directory
mkdir -p $REPORT_DIR

echo -e "${BLUE}🚀 Newman Test Runner for Blacklist Microservice${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if collection file exists
if [ ! -f "$COLLECTION_FILE" ]; then
    echo -e "${RED}❌ Collection file not found: $COLLECTION_FILE${NC}"
    exit 1
fi

# Check if Newman is installed
if ! command -v newman &> /dev/null; then
    echo -e "${RED}❌ Newman is not installed. Please install it with: npm install -g newman${NC}"
    exit 1
fi

# Check if server is running
echo -e "${YELLOW}🔍 Checking if server is running at $BASE_URL...${NC}"
if ! curl -s "$BASE_URL/blacklists/ping" > /dev/null; then
    echo -e "${RED}❌ Server is not running at $BASE_URL${NC}"
    echo -e "${YELLOW}💡 Please start the server first with:${NC}"
    echo -e "   cd api && source ../venv/bin/activate && python src/app.py"
    exit 1
fi

echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# Run Newman tests
echo -e "${BLUE}🧪 Running Newman tests...${NC}"
echo ""

newman run "$COLLECTION_FILE" \
    --global-var "base_url=$BASE_URL" \
    --global-var "secret_token=$SECRET_TOKEN" \
    --reporters cli,html,json \
    --reporter-html-export "$REPORT_DIR/newman_report_$TIMESTAMP.html" \
    --reporter-json-export "$REPORT_DIR/newman_report_$TIMESTAMP.json" \
    --timeout-request 10000 \
    --timeout-script 10000 \
    --bail

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed successfully!${NC}"
    echo -e "${GREEN}📊 HTML Report: $REPORT_DIR/newman_report_$TIMESTAMP.html${NC}"
    echo -e "${GREEN}📊 JSON Report: $REPORT_DIR/newman_report_$TIMESTAMP.json${NC}"
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Check the output above.${NC}"
    echo -e "${YELLOW}📊 HTML Report: $REPORT_DIR/newman_report_$TIMESTAMP.html${NC}"
    echo -e "${YELLOW}📊 JSON Report: $REPORT_DIR/newman_report_$TIMESTAMP.json${NC}"
    exit 1
fi
