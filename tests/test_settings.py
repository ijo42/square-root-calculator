"""Tests for settings management."""

import pytest
import tempfile
from pathlib import Path
from square_root_calculator.core.settings import Settings


class TestSettings:
    """Test Settings class."""

    def test_create_settings(self, settings):
        """Test creating settings instance."""
        assert settings is not None
        assert isinstance(settings.settings, dict)

    def test_default_settings(self, settings):
        """Test default settings values."""
        assert settings.get("theme") == "light"
        assert settings.get("precision") == 4
        assert settings.get("show_exact_precision") == False
        assert settings.get("show_negative_roots") == False
        assert settings.get("language") == "en"

    def test_get_setting(self, settings):
        """Test getting a setting."""
        value = settings.get("theme")
        assert value == "light"

    def test_get_missing_setting_with_default(self, settings):
        """Test getting non-existent setting with default."""
        value = settings.get("nonexistent", "default_value")
        assert value == "default_value"

    def test_set_setting(self, settings):
        """Test setting a value."""
        settings.set("theme", "dark")
        assert settings.get("theme") == "dark"

    def test_get_all_settings(self, settings):
        """Test getting all settings."""
        all_settings = settings.get_all()
        assert isinstance(all_settings, dict)
        assert "theme" in all_settings
        assert "precision" in all_settings

    def test_reset_settings(self, settings):
        """Test resetting to defaults."""
        settings.set("theme", "dark")
        settings.set("precision", 100)
        settings.reset()
        assert settings.get("theme") == "light"
        assert settings.get("precision") == 4

    def test_settings_persistence(self):
        """Test that settings persist across instances."""
        # Create temp directory for settings
        with tempfile.TemporaryDirectory() as tmpdir:
            settings1 = Settings()
            settings1.settings_file = Path(tmpdir) / "settings.json"
            settings1.set("theme", "dark")
            settings1.save()

            settings2 = Settings()
            settings2.settings_file = Path(tmpdir) / "settings.json"
            settings2.load()

            assert settings2.get("theme") == "dark"
