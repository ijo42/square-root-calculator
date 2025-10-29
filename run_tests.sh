#!/bin/bash
# Скрипт запуска тестов для Linux/macOS с использованием uv
# Test execution script for Linux/macOS using uv package manager
# Запускает pytest с покрытием кода и генерирует HTML отчёты
# Runs pytest with coverage and generates HTML reports

set -e

echo "======================================================"
echo "Square Root Calculator Test Suite"
echo "Набор тестов калькулятора квадратных корней"
echo "======================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ uv не установлен / uv is not installed${NC}"
    echo ""
    echo "Установите uv / Install uv:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Или используйте / Or use:"
    echo "  pip install uv"
    exit 1
fi

echo -e "${GREEN}✓ uv найден / uv found${NC}"
echo ""

# Sync dependencies with uv
echo -e "${BLUE}Синхронизация зависимостей с uv...${NC}"
echo -e "${BLUE}Syncing dependencies with uv...${NC}"
uv sync --dev > /dev/null 2>&1

echo -e "${GREEN}✓ Зависимости установлены / Dependencies installed${NC}"
echo ""

# Run tests
echo -e "${GREEN}Запуск тестов с покрытием...${NC}"
echo -e "${GREEN}Running tests with coverage...${NC}"
echo ""

uv run pytest \
    --verbose \
    --cov=src/square_root_calculator \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml

# Check test result
TEST_RESULT=$?

echo ""
echo "======================================================"
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Все тесты пройдены! / All tests passed!${NC}"
else
    echo -e "${RED}✗ Некоторые тесты не прошли / Some tests failed${NC}"
fi
echo "======================================================"
echo ""

# Display coverage report location
if [ -d "htmlcov" ]; then
    echo -e "${BLUE}HTML отчёт о покрытии создан:${NC}"
    echo -e "${BLUE}HTML coverage report generated:${NC}"
    echo "  file://$(pwd)/htmlcov/index.html"
    echo ""
    echo -e "${BLUE}Для просмотра откройте:${NC}"
    echo -e "${BLUE}To view the report, open:${NC}"
    echo "  htmlcov/index.html"
fi

echo ""
echo -e "${BLUE}XML отчёт о покрытии: coverage.xml${NC}"
echo -e "${BLUE}XML coverage report: coverage.xml${NC}"
echo ""

exit $TEST_RESULT
