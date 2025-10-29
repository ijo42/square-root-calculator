"""Application settings and configuration management."""

import json
from pathlib import Path
from typing import Any, Dict


class Settings:
    """Manages application settings with persistence."""
    
    DEFAULT_SETTINGS = {
        'theme': 'light',  # 'light' or 'dark'
        'precision': 4,
        'show_exact_precision': False,
        'show_negative_roots': False,
        'language': 'en',
    }
    
    def __init__(self):
        """Initialize settings manager."""
        self.settings_file = Path.home() / '.square_root_calculator' / 'settings.json'
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self):
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
        except Exception as e:
            print(f"Could not load settings: {e}")
    
    def save(self):
        """Save settings to file."""
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings."""
        return self.settings.copy()
    
    def reset(self):
        """Reset to default settings."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
