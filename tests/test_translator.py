"""Tests for translator and localization."""

import pytest
from square_root_calculator.locales.translator import Translator


class TestTranslator:
    """Test Translator class."""
    
    def test_create_translator_english(self, translator_en):
        """Test creating English translator."""
        assert translator_en.language == 'en'
    
    def test_create_translator_russian(self, translator_ru):
        """Test creating Russian translator."""
        assert translator_ru.language == 'ru'
    
    def test_get_translation_english(self, translator_en):
        """Test getting English translations."""
        assert translator_en.get('app_title') == 'Square Root Calculator'
        assert translator_en.get('calculate_button') == 'Calculate'
    
    def test_get_translation_russian(self, translator_ru):
        """Test getting Russian translations."""
        assert translator_ru.get('app_title') == 'Калькулятор квадратного корня'
        assert translator_ru.get('calculate_button') == 'Вычислить'
    
    def test_get_missing_key(self, translator_en):
        """Test getting non-existent key returns key itself."""
        assert translator_en.get('nonexistent_key') == 'nonexistent_key'
    
    def test_set_language(self, translator_en):
        """Test changing language."""
        translator_en.set_language('ru')
        assert translator_en.language == 'ru'
        assert translator_en.get('app_title') == 'Калькулятор квадратного корня'
    
    def test_invalid_language_defaults_to_english(self):
        """Test invalid language code defaults to English."""
        translator = Translator('invalid')
        assert translator.language == 'en'
    
    def test_new_theme_keys_exist(self, translator_en):
        """Test that new theme-related keys exist."""
        assert translator_en.get('theme') == 'Theme'
        assert translator_en.get('theme_light') == 'Light Theme'
        assert translator_en.get('theme_dark') == 'Dark Theme'
    
    def test_new_settings_keys_exist(self, translator_en):
        """Test that new settings keys exist."""
        assert translator_en.get('settings') == 'Settings'
        assert translator_en.get('show_exact_precision') == 'Show Exact Precision Field'
        assert translator_en.get('show_negative_roots') == 'Show Negative Roots'
    
    def test_alternative_forms_keys_exist(self, translator_en):
        """Test that alternative forms keys exist."""
        assert translator_en.get('polar_form') == 'Polar form:'
        assert translator_en.get('exponential_form') == 'Exponential form:'
        assert translator_en.get('alternative_forms') == 'Alternative Forms:'
    
    def test_user_manual_key_exists(self, translator_en):
        """Test that user manual key exists."""
        assert translator_en.get('user_manual') == 'User Manual'
    
    def test_get_available_languages(self, translator_en):
        """Test getting available languages."""
        languages = translator_en.get_available_languages()
        assert 'en' in languages
        assert 'ru' in languages
        assert languages['en'] == 'English'
