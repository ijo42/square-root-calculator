# Testing Guide

Comprehensive guide for running tests in the Square Root Calculator project.

## Quick Start

### Linux/macOS

```bash
# Make script executable
chmod +x run_tests.sh

# Run all tests with coverage
./run_tests.sh
```

### Windows

```cmd
# Run all tests with coverage
run_tests.bat
```

### Cross-platform (Python script)

```bash
# Works on all platforms
python run_tests.py
```

## Test Scripts Overview

### 1. Full Test Suite with Coverage

**`run_tests.sh` (Linux/macOS)** or **`run_tests.bat` (Windows)**

Features:
- Creates virtual environment if needed
- Installs all dependencies
- Runs complete test suite
- Generates HTML coverage report
- Generates XML coverage report (for CI/CD)
- Shows terminal coverage summary
- Color-coded output

Output files:
- `htmlcov/index.html` - Interactive HTML coverage report
- `coverage.xml` - XML report for CI tools
- `.coverage` - Coverage database

### 2. Cross-platform Python Runner

**`run_tests.py`**

Features:
- Works on Windows, Linux, and macOS
- Checks for virtual environment
- Installs dependencies
- Runs tests with coverage
- Pure Python implementation

Usage:
```bash
python run_tests.py
```

### 3. Quick Test Runner

**`test_quick.sh` (Linux/macOS)** or **`test_quick.bat` (Windows)**

Features:
- Fast test execution
- No coverage overhead
- Run specific tests or all tests
- Useful during development

Usage:
```bash
# Run all tests
./test_quick.sh

# Run specific test file
./test_quick.sh tests/test_calculator.py

# Run specific test function
./test_quick.sh tests/test_calculator.py::TestSquareRootCalculator::test_sqrt_real_perfect_square
```

## Manual Test Commands

### Basic Test Execution

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Very verbose output
pytest -vv
```

### Run Specific Tests

```bash
# Run single test file
pytest tests/test_calculator.py

# Run specific test class
pytest tests/test_calculator.py::TestSquareRootCalculator

# Run specific test function
pytest tests/test_calculator.py::TestSquareRootCalculator::test_sqrt_real_perfect_square

# Run tests matching pattern
pytest -k "sqrt_real"
```

### Coverage Options

```bash
# Run with coverage (terminal output)
pytest --cov=src/square_root_calculator

# Generate HTML report
pytest --cov=src/square_root_calculator --cov-report=html

# Generate XML report (for CI)
pytest --cov=src/square_root_calculator --cov-report=xml

# Show missing lines
pytest --cov=src/square_root_calculator --cov-report=term-missing

# All reports at once
pytest --cov=src/square_root_calculator --cov-report=html --cov-report=xml --cov-report=term-missing
```

### Test Output Options

```bash
# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Show test durations
pytest --durations=10
```

## Understanding Coverage Reports

### HTML Coverage Report

After running tests with HTML coverage:

1. Open `htmlcov/index.html` in your browser
2. Click on any file to see line-by-line coverage
3. Red lines = not covered by tests
4. Green lines = covered by tests
5. Yellow lines = partially covered (branches)

### Terminal Coverage Report

The terminal shows:
- **Statements**: Total lines of code
- **Miss**: Lines not covered
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

Example output:
```
Name                                           Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------------
src/square_root_calculator/core/calculator.py    150     10    93%   45-48, 122-125
src/square_root_calculator/core/history.py        45      2    96%   67-68
src/square_root_calculator/locales/translator.py  38      0   100%
-----------------------------------------------------------------------------
TOTAL                                             350     15    96%
```

## Test Structure

```
tests/
├── conftest.py              # Fixtures and test configuration
├── test_calculator.py       # Calculator core tests (16 tests)
├── test_history.py          # History manager tests (11 tests)
├── test_translator.py       # Translation tests (13 tests)
└── test_settings.py         # Settings tests (9 tests)
```

## Writing New Tests

### Using Fixtures

```python
def test_example(calculator, translator_en):
    """Test using fixtures from conftest.py."""
    result = calculator.sqrt_real(4)
    assert result == Decimal('2')
    assert translator_en.get('app_title') == 'Square Root Calculator'
```

### Available Fixtures

- `calculator` - SquareRootCalculator instance (precision=10)
- `translator_en` - English translator
- `translator_ru` - Russian translator
- `history_manager` - HistoryManager instance (max 10 entries)
- `settings` - Settings instance with defaults

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use descriptive names: `test_sqrt_real_perfect_square`

## CI/CD Integration

The project includes GitHub Actions workflow (`.github/workflows/ci.yml`):

### On Pull Requests:
1. Runs all tests
2. Generates coverage reports
3. Uploads to Codecov
4. Archives HTML reports
5. Runs linting checks

### View Results:
- GitHub Actions tab in repository
- Coverage trends on Codecov
- Download artifacts for HTML reports

## Troubleshooting

### Tests Not Found

```bash
# Ensure you're in the project root
cd /path/to/square-root-calculator

# Check Python path
python -c "import sys; print(sys.path)"
```

### Import Errors

```bash
# Install in development mode
pip install -e ".[dev]"

# Or install just test dependencies
pip install pytest pytest-cov pytest-qt
```

### Virtual Environment Issues

```bash
# Create fresh virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Coverage Not Working

```bash
# Ensure pytest-cov is installed
pip install pytest-cov

# Verify installation
pytest --version
```

## Performance Tips

1. **Use quick runner during development**
   ```bash
   ./test_quick.sh tests/test_calculator.py
   ```

2. **Run only failed tests**
   ```bash
   pytest --lf  # last-failed
   pytest --ff  # failed-first
   ```

3. **Parallel execution** (install pytest-xdist)
   ```bash
   pip install pytest-xdist
   pytest -n auto  # auto-detect CPU cores
   ```

4. **Cache test results**
   ```bash
   pytest --cache-show  # show cache
   pytest --cache-clear  # clear cache
   ```

## Test Coverage Goals

Current coverage: **~96%** (49 test cases)

Target areas for improvement:
- Edge cases in complex number calculations
- Error handling scenarios
- UI event handlers (requires pytest-qt)
- Update checker network failures

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [pytest-qt documentation](https://pytest-qt.readthedocs.io/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
