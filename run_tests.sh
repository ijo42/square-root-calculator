#!/bin/bash
# Test execution script for Linux/macOS
# Runs pytest with coverage and generates HTML reports

set -e

echo "=================================="
echo "Square Root Calculator Test Suite"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -e ".[dev]" > /dev/null 2>&1

# Run tests
echo ""
echo -e "${GREEN}Running tests with coverage...${NC}"
echo ""

pytest \
    --verbose \
    --cov=src/square_root_calculator \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml

# Check test result
TEST_RESULT=$?

echo ""
echo "=================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${YELLOW}✗ Some tests failed${NC}"
fi
echo "=================================="
echo ""

# Display coverage report location
if [ -d "htmlcov" ]; then
    echo -e "${BLUE}HTML coverage report generated:${NC}"
    echo "  file://$(pwd)/htmlcov/index.html"
    echo ""
    echo -e "${BLUE}To view the report, open:${NC}"
    echo "  htmlcov/index.html"
fi

echo ""
echo -e "${BLUE}XML coverage report:${NC} coverage.xml"
echo ""

exit $TEST_RESULT
