#!/usr/bin/env python3
"""
Cross-platform test runner script
Runs pytest with coverage and generates HTML reports
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Run tests with coverage."""
    print("=" * 50)
    print("Square Root Calculator Test Suite")
    print("=" * 50)
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if running in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("⚠️  Warning: Not running in a virtual environment")
        print("   Consider activating venv first:")
        print("   Linux/macOS: source .venv/bin/activate")
        print("   Windows: .venv\\Scripts\\activate")
        print()
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return 1
    
    print()
    print("Running tests with coverage...")
    print()
    
    # Run pytest
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
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
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 50)
    print()
    
    # Display coverage report info
    htmlcov_dir = project_root / "htmlcov"
    if htmlcov_dir.exists():
        index_file = htmlcov_dir / "index.html"
        print("HTML coverage report generated:")
        print(f"  file://{index_file.absolute()}")
        print()
        print("To view the report, open:")
        print(f"  {index_file.relative_to(project_root)}")
    
    print()
    print("XML coverage report: coverage.xml")
    print()
    
    return 0 if test_passed else 1


if __name__ == "__main__":
    sys.exit(main())
