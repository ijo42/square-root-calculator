@echo off
REM Скрипт запуска тестов для Windows с использованием uv
REM Test execution script for Windows using uv package manager
REM Запускает pytest с покрытием кода и генерирует HTML отчёты
REM Runs pytest with coverage and generates HTML reports

echo ======================================================
echo Square Root Calculator Test Suite
echo Набор тестов калькулятора квадратных корней
echo ======================================================
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [31m✗ uv не установлен / uv is not installed[0m
    echo.
    echo Установите uv / Install uv:
    echo   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    echo Или используйте / Or use:
    echo   pip install uv
    exit /b 1
)

echo [32m✓ uv найден / uv found[0m
echo.

REM Sync dependencies with uv
echo [34mСинхронизация зависимостей с uv...[0m
echo [34mSyncing dependencies with uv...[0m
uv sync --dev >nul 2>&1

echo [32m✓ Зависимости установлены / Dependencies installed[0m
echo.

REM Run tests
echo.
echo [32mЗапуск тестов с покрытием...[0m
echo [32mRunning tests with coverage...[0m
echo.

uv run pytest ^
    --verbose ^
    --cov=src/square_root_calculator ^
    --cov-report=html ^
    --cov-report=term-missing ^
    --cov-report=xml

REM Store test result
set TEST_RESULT=%ERRORLEVEL%

echo.
echo ======================================================
if %TEST_RESULT% equ 0 (
    echo [32m✓ Все тесты пройдены! / All tests passed![0m
) else (
    echo [31m✗ Некоторые тесты не прошли / Some tests failed[0m
)
echo ======================================================
echo.

REM Display coverage report location
if exist "htmlcov" (
    echo [34mHTML отчёт о покрытии создан:[0m
    echo [34mHTML coverage report generated:[0m
    echo   file:///%CD%\htmlcov\index.html
    echo.
    echo [34mДля просмотра откройте:[0m
    echo [34mTo view the report, open:[0m
    echo   htmlcov\index.html
)

echo.
echo [34mXML отчёт о покрытии: coverage.xml[0m
echo [34mXML coverage report: coverage.xml[0m
echo.

exit /b %TEST_RESULT%
