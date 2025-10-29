"""Application settings and configuration management.

Управление настройками и конфигурацией приложения.
"""

import json
from pathlib import Path
from typing import Any, Dict


class Settings:
    """Manages application settings with persistence.
    
    Управляет настройками приложения с сохранением.
    """
    
    DEFAULT_SETTINGS = {
        'theme': 'light',  # 'light' or 'dark'
        'precision': 4,
        'show_exact_precision': False,
        'show_negative_roots': False,
        'language': 'en',
    }
    
    def __init__(self):
        """Initialize settings manager.
        
        Инициализировать менеджер настроек.
        """
        self.settings_file = Path.home() / '.square_root_calculator' / 'settings.json'
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self):
        """Load settings from file.
        
        Загрузить настройки из файла.
        """
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
        except Exception as e:
            print(f"Could not load settings: {e}")
    
    def save(self):
        """Save settings to file.
        
        Сохранить настройки в файл.
        """
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value.
        
        Получить значение настройки.
        
        Args:
            key: Setting key
                Ключ настройки
            default: Default value if key not found
                    Значение по умолчанию, если ключ не найден
        
        Returns:
            Setting value or default
            Значение настройки или значение по умолчанию
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value.
        
        Установить значение настройки.
        
        Args:
            key: Setting key
                Ключ настройки
            value: Setting value
                  Значение настройки
        """
        self.settings[key] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings.
        
        Получить все настройки.
        
        Returns:
            Dictionary of all settings
            Словарь всех настроек
        """
        return self.settings.copy()
    
    def reset(self):
        """Reset to default settings.
        
        Сбросить к настройкам по умолчанию.
        """
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
