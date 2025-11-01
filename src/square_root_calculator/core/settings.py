"""Application settings and configuration management.

Управление настройками и конфигурацией приложения.
"""

import json
import locale
import re
import sys
from pathlib import Path
from typing import Any, Dict


class Settings:
    """Manages application settings with persistence.

    Управляет настройками приложения с сохранением.
    """

    DEFAULT_SETTINGS = {
        "theme": "light",  # 'light' or 'dark'
        "precision": 4,
        "show_exact_precision": False,
        "show_negative_roots": False,
        "language": "en",
        "skipped_updates": [],  # List of version numbers that user chose to skip
    }

    def __init__(self) -> None:
        """Initialize settings manager.

        Инициализировать менеджер настроек.
        """
        self.settings_file = Path.home() / ".square_root_calculator" / "settings.json"
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()

        # Apply system defaults if settings file doesn't exist or settings are default
        self._apply_system_defaults()

    def _apply_system_defaults(self) -> None:
        """Apply system defaults for language and theme if not explicitly set.

        Применить системные значения по умолчанию для языка и темы, если они не установлены явно.
        """
        # Only apply system defaults if using the default settings
        # (i.e., settings file didn't exist or didn't have these keys)

        # Detect system language
        if self.settings.get("language") == self.DEFAULT_SETTINGS["language"]:
            system_lang = self._get_system_language()
            if system_lang in ["en", "ru"]:
                self.settings["language"] = system_lang

        # Detect system theme (dark mode)
        if self.settings.get("theme") == self.DEFAULT_SETTINGS["theme"]:
            system_theme = self._get_system_theme()
            if system_theme:
                self.settings["theme"] = system_theme

    def _get_system_language(self) -> str:
        """Get system language.

        Получить системный язык.

        Returns:
            Language code ('en', 'ru', etc.)
        """
        try:
            # Try to get system locale using the recommended approach
            system_locale = locale.getlocale()[0]
            if system_locale:
                # Extract language code (e.g., 'en_US' -> 'en', 'ru_RU' -> 'ru')
                lang_code = system_locale.split("_")[0].lower()
                return lang_code
        except Exception:
            pass
        return "en"

    def _get_system_theme(self) -> str:
        """Get system theme (light/dark mode).

        Получить системную тему (светлый/тёмный режим).

        Returns:
            Theme name ('light' or 'dark')
        """
        try:
            # Try to detect dark mode on different platforms
            if sys.platform == "win32":  # Windows
                try:
                    import winreg

                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                    )
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    winreg.CloseKey(key)
                    return "light" if value == 1 else "dark"
                except Exception:
                    pass
            elif sys.platform.startswith("linux"):  # Linux
                # Try to detect from GTK settings
                gtk_settings = Path.home() / ".config" / "gtk-3.0" / "settings.ini"
                if gtk_settings.exists():
                    with open(gtk_settings) as f:
                        content = f.read()
                        # Check for dark theme preference or dark theme name
                        if (
                            "gtk-application-prefer-dark-theme=1" in content
                            or re.search(
                                r"gtk-theme-name.*dark", content, re.IGNORECASE
                            )
                        ):
                            return "dark"
        except Exception:
            pass

        return "light"  # Default to light theme

    def load(self) -> None:
        """Load settings from file.

        Загрузить настройки из файла.
        """
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r") as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
        except Exception as e:
            print(f"Could not load settings: {e}")

    def save(self) -> None:
        """Save settings to file.

        Сохранить настройки в файл.
        """
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, "w") as f:
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

    def set(self, key: str, value: Any) -> None:
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

    def reset(self) -> None:
        """Reset to default settings.

        Сбросить к настройкам по умолчанию.
        """
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
