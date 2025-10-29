# Makefile for Square Root Calculator
# Convenient shortcuts for common development tasks

.PHONY: help install test test-quick coverage clean run lint format

help:
	@echo "Square Root Calculator - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run all tests with coverage"
	@echo "  test-quick   - Run tests quickly (no coverage)"
	@echo "  coverage     - Generate and open HTML coverage report"
	@echo "  run          - Run the application"
	@echo "  lint         - Run code linters"
	@echo "  format       - Format code with black"
	@echo "  clean        - Remove generated files"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -e ".[dev]"

test:
	@echo "Running tests with coverage..."
	pytest --cov=src/square_root_calculator --cov-report=html --cov-report=term-missing

test-quick:
	@echo "Running tests (quick)..."
	pytest -v

coverage: test
	@echo "Opening coverage report..."
	@which xdg-open > /dev/null && xdg-open htmlcov/index.html || \
	which open > /dev/null && open htmlcov/index.html || \
	echo "Please open htmlcov/index.html manually"

run:
	@echo "Starting Square Root Calculator..."
	python main.py

lint:
	@echo "Running linters..."
	@which flake8 > /dev/null && flake8 src/ tests/ || echo "flake8 not installed"
	@which black > /dev/null && black --check src/ tests/ || echo "black not installed"

format:
	@echo "Formatting code..."
	@which black > /dev/null && black src/ tests/ || echo "black not installed (pip install black)"

clean:
	@echo "Cleaning generated files..."
	rm -rf htmlcov/
	rm -f coverage.xml
	rm -f .coverage
	rm -rf .pytest_cache/
	rm -rf src/square_root_calculator.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete"
