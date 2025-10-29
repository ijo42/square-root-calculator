@echo off
REM Test execution script for Windows
REM Runs pytest with coverage and generates HTML reports

echo ==================================
echo Square Root Calculator Test Suite
echo ==================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Creating...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -e ".[dev]" >nul 2>&1

REM Run tests
echo.
echo Running tests with coverage...
echo.

pytest ^
    --verbose ^
    --cov=src/square_root_calculator ^
    --cov-report=html ^
    --cov-report=term-missing ^
    --cov-report=xml

REM Store test result
set TEST_RESULT=%ERRORLEVEL%

echo.
echo ==================================
if %TEST_RESULT% equ 0 (
    echo [32m✓ All tests passed![0m
) else (
    echo [33m✗ Some tests failed[0m
)
echo ==================================
echo.

REM Display coverage report location
if exist "htmlcov" (
    echo HTML coverage report generated:
    echo   file:///%CD%\htmlcov\index.html
    echo.
    echo To view the report, open:
    echo   htmlcov\index.html
)

echo.
echo XML coverage report: coverage.xml
echo.

exit /b %TEST_RESULT%
