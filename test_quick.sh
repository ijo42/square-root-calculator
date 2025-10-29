#!/bin/bash
# Quick test runner - runs specific test files or all tests

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}Quick Test Runner${NC}"
echo ""

# Activate venv if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ $# -eq 0 ]; then
    echo "Running all tests..."
    pytest -v
else
    echo "Running: $@"
    pytest -v "$@"
fi

TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    echo -e "${GREEN}✗ Tests failed${NC}"
fi

exit $TEST_RESULT
