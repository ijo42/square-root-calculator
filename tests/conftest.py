"""Test configuration and fixtures for pytest."""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))


@pytest.fixture
def calculator():
    """Fixture providing a calculator instance."""
    from square_root_calculator.core.calculator import SquareRootCalculator
    return SquareRootCalculator(precision=10)


@pytest.fixture
def translator_en():
    """Fixture providing English translator."""
    from square_root_calculator.locales.translator import Translator
    return Translator('en')


@pytest.fixture
def translator_ru():
    """Fixture providing Russian translator."""
    from square_root_calculator.locales.translator import Translator
    return Translator('ru')


@pytest.fixture
def history_manager():
    """Fixture providing history manager."""
    from square_root_calculator.core.history import HistoryManager
    return HistoryManager(max_entries=10)


@pytest.fixture
def settings():
    """Fixture providing settings instance."""
    from square_root_calculator.core.settings import Settings
    s = Settings()
    # Reset to defaults for testing
    s.settings = s.DEFAULT_SETTINGS.copy()
    return s
