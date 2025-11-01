"""Square Root Calculator - A comprehensive calculator for computing square roots."""

import sys
from pathlib import Path


def get_version() -> str:
    """Get version from pyproject.toml.

    Загрузить версию из pyproject.toml.

    Returns:
        Version string
        Строка версии
    """
    try:
        # For PyInstaller bundled app, use _MEIPASS
        if getattr(sys, "frozen", False):
            base_path = Path(sys._MEIPASS)
            pyproject_path = base_path / "pyproject.toml"
        else:
            # Development mode: find pyproject.toml
            current_dir = Path(__file__).parent
            pyproject_path = None
            # Go up to find pyproject.toml (should be 2 levels up from src/square_root_calculator)
            for _ in range(5):  # Try up to 5 levels up
                test_path = current_dir / "pyproject.toml"
                if test_path.exists():
                    pyproject_path = test_path
                    break
                current_dir = current_dir.parent

        if pyproject_path and pyproject_path.exists():
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
    except Exception:
        pass

    # Fallback version if pyproject.toml not found
    return "0.0.0"


__version__ = get_version()
