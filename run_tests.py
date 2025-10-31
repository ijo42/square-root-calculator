#!/usr/bin/env python3
"""
Скрипт запуска тестов с использованием uv (кроссплатформенный).
Cross-platform test runner script using uv package manager.

Запускает pytest с покрытием кода и генерирует HTML отчёты.
Runs pytest with coverage and generates HTML reports.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def main():
    """
    Запустить тесты с покрытием кода.
    Run tests with coverage.
    """
    print("=" * 50)
    print("Square Root Calculator Test Suite")
    print("Набор тестов калькулятора квадратных корней")
    print("=" * 50)
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if uv is installed
    if not shutil.which("uv"):
        print("✗ uv не установлен / uv is not installed")
        print()
        print("Установите uv / Install uv:")
        print("  curl -LsSf https://astral.sh/uv/install.sh | sh  (Linux)")
        print("  powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"  (Windows)")
        print()
        print("Или используйте / Or use:")
        print("  pip install uv")
        return 1
    
    print("✓ uv найден / uv found")
    print()
    
    # Sync dependencies with uv
    print("Синхронизация зависимостей с uv...")
    print("Syncing dependencies with uv...")
    try:
        subprocess.run(
            ["uv", "sync", "--dev"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ Зависимости установлены / Dependencies installed")
    except subprocess.CalledProcessError:
        print("✗ Не удалось установить зависимости / Failed to install dependencies")
        return 1
    
    print()
    print("Запуск тестов с покрытием...")
    print("Running tests with coverage...")
    print()
    
    # Run pytest via uv
    try:
        result = subprocess.run(
            [
                "uv", "run", "pytest",
                "--verbose",
                "--cov=src/square_root_calculator",
                "--cov-report=html",
                "--cov-report=term-missing",
                "--cov-report=xml",
            ],
            check=True
        )
        test_passed = True
    except subprocess.CalledProcessError:
        test_passed = False
    
    print()
    print("=" * 50)
    if test_passed:
        print("✓ Все тесты пройдены! / All tests passed!")
    else:
        print("✗ Некоторые тесты не прошли / Some tests failed")
    print("=" * 50)
    print()
    
    # Display coverage report info
    htmlcov_dir = project_root / "htmlcov"
    if htmlcov_dir.exists():
        index_file = htmlcov_dir / "index.html"
        print("HTML отчёт о покрытии создан:")
        print("HTML coverage report generated:")
        print(f"  file://{index_file.absolute()}")
        print()
        print("Для просмотра откройте:")
        print("To view the report, open:")
        print(f"  {index_file.relative_to(project_root)}")
    
    print()
    print("XML отчёт о покрытии: coverage.xml")
    print("XML coverage report: coverage.xml")
    print()
    
    return 0 if test_passed else 1


if __name__ == "__main__":
    sys.exit(main())
