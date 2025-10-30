"""Square Root Calculator - A comprehensive calculator for computing square roots."""

import os
from pathlib import Path


def get_version() -> str:
    """Get version from pyproject.toml.
    
    Загрузить версию из pyproject.toml.
    
    Returns:
        Version string
        Строка версии
    """
    try:
        # Try to find pyproject.toml
        # Start from this file's directory and go up
        current_dir = Path(__file__).parent
        
        # Go up to find pyproject.toml (should be 2 levels up from src/square_root_calculator)
        for _ in range(5):  # Try up to 5 levels up
            pyproject_path = current_dir / "pyproject.toml"
            if pyproject_path.exists():
                # Read and parse pyproject.toml
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("version"):
                            # Extract version string: version = "0.2.0"
                            parts = line.split("=")
                            if len(parts) == 2:
                                version = parts[1].strip().strip('"').strip("'")
                                return version
                break
            current_dir = current_dir.parent
    except Exception:
        pass
    
    # Fallback version if pyproject.toml not found
    return "0.2.0"


__version__ = get_version()

