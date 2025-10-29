@echo off
REM Quick test runner for Windows - runs specific test files or all tests

echo Quick Test Runner
echo.

REM Activate venv if it exists
if exist ".venv" (
    call .venv\Scripts\activate.bat
)

if "%~1"=="" (
    echo Running all tests...
    pytest -v
) else (
    echo Running: %*
    pytest -v %*
)

set TEST_RESULT=%ERRORLEVEL%

echo.
if %TEST_RESULT% equ 0 (
    echo [32m✓ Tests passed[0m
) else (
    echo [33m✗ Tests failed[0m
)

exit /b %TEST_RESULT%
