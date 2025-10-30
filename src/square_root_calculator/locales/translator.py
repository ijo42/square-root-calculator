"""Localization system for multilingual support.

Система локализации для поддержки нескольких языков.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple


class Translator:
    """Simple translation system supporting multiple languages.

    Простая система перевода с поддержкой нескольких языков.
    """

    # Translations are now loaded from JSON files
    TRANSLATIONS: Dict[str, Dict[str, str]] = {}

    def __init__(self, language: str = "en"):
        """Initialize translator with specified language.

        Инициализировать переводчик с указанным языком.

        Args:
            language: Language code ('en' or 'ru')
                     Код языка ('en' или 'ru')
        """
        # Load built-in translations first
        self._load_builtin_translations()

        self.language = language if language in self.TRANSLATIONS else "en"
        self.custom_translations_loaded = False
        self.load_custom_translations()

    def _load_builtin_translations(self):
        """Load built-in translations from JSON files in locales folder.

        Загрузить встроенные переводы из JSON файлов в папке locales.
        """
        locales_dir = Path(__file__).parent

        for json_file in locales_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    translation_data = json.load(f)
                    lang_code = json_file.stem
                    self.TRANSLATIONS[lang_code] = translation_data
            except (json.JSONDecodeError, Exception) as e:
                print(f"Failed to load built-in translation from {json_file}: {e}")

    def load_custom_translations(self):
        """Load custom translations from JSON files in translations folder.

        Загрузить пользовательские переводы из JSON файлов в папке translations.
        """
        try:
            # Look for translations folder in current directory and app directory
            translations_paths = [
                Path("translations"),
                Path.home() / ".square_root_calculator" / "translations",
            ]

            for translations_dir in translations_paths:
                if translations_dir.exists() and translations_dir.is_dir():
                    for json_file in translations_dir.glob("*.json"):
                        # Skip example files
                        if json_file.name.endswith(".example"):
                            continue

                        try:
                            with open(json_file, "r", encoding="utf-8") as f:
                                custom_trans = json.load(f)
                                # Assume filename is the language code (e.g., de.json for German)
                                lang_code = json_file.stem

                                if lang_code in self.TRANSLATIONS:
                                    # Update existing language with custom translations
                                    self.TRANSLATIONS[lang_code].update(custom_trans)
                                else:
                                    # Add new language
                                    self.TRANSLATIONS[lang_code] = custom_trans

                                self.custom_translations_loaded = True
                        except (json.JSONDecodeError, Exception) as e:
                            print(f"Failed to load translation from {json_file}: {e}")
        except Exception as e:
            print(f"Error loading custom translations: {e}")

    def reload_translations(self):
        """Reload all custom translations from JSON files.

        Перезагрузить все пользовательские переводы из JSON файлов.
        """
        # Clear translations and reload
        self.TRANSLATIONS.clear()
        self._load_builtin_translations()
        self.load_custom_translations()

    def set_language(self, language: str):
        """Set the current language.

        Установить текущий язык.

        Args:
            language: Language code
                     Код языка
        """
        if language in self.TRANSLATIONS:
            self.language = language

    def get(self, key: str) -> str:
        """Get translated string for the current language.

        Получить переведенную строку для текущего языка.

        Args:
            key: Translation key
                Ключ перевода

        Returns:
            Translated string or key if not found
            Переведенная строка или ключ, если не найден
        """
        return self.TRANSLATIONS.get(self.language, {}).get(key, key)

    def get_available_languages(self) -> List[Tuple[str, str]]:
        """Get list of available languages.

        Получить список доступных языков.

        Returns:
            List of tuples (language_code, language_name)
            Список кортежей (код_языка, название_языка)
        """
        languages = []
        for lang_code, translations in self.TRANSLATIONS.items():
            # Get language name from _language_name key, or fallback to code
            lang_name = translations.get("_language_name", lang_code.upper())
            languages.append((lang_code, lang_name))

        # Sort by language code
        languages.sort(key=lambda x: x[0])
        return languages
