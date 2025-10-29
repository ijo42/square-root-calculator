"""Localization system for multilingual support."""

from typing import Dict


class Translator:
    """Simple translation system supporting multiple languages."""
    
    TRANSLATIONS: Dict[str, Dict[str, str]] = {
        'en': {
            'app_title': 'Square Root Calculator',
            'input_label': 'Input Value:',
            'real_part_label': 'Real Part:',
            'imag_part_label': 'Imaginary Part:',
            'precision_label': 'Precision:',
            'precision_control': 'Precision Control',
            'exact_value': 'Exact value (1-1000):',
            'mode_label': 'Calculation Mode:',
            'mode_real': 'Real Numbers',
            'mode_complex': 'Complex Numbers',
            'calculate_button': 'Calculate',
            'clear_button': 'Clear',
            'result_label': 'Result',
            'error_title': 'Error',
            'invalid_input': 'Invalid input. Please enter a valid number.',
            'negative_real': 'Cannot calculate square root of negative real number. Switch to Complex mode.',
            'invalid_precision': 'Precision must be a positive integer.',
            'calculation_error': 'Calculation error: {}',
            'language': 'Language:',
            'language_menu': 'Language',
            'english': 'English',
            'russian': 'Русский',
            'about': 'About',
            'about_text': 'Square Root Calculator v0.1.0\n\nA comprehensive calculator for computing square roots of real and complex numbers with arbitrary precision.\n\nFeatures:\n- Real and complex number support\n- Arbitrary precision\n- Multilingual interface',
            'help': 'Help',
            'help_text': 'How to use:\n\n1. Choose calculation mode (Real or Complex tab)\n2. Enter the input value(s)\n3. Set desired precision using slider or spinbox\n4. Click Calculate\n\nReal Mode: Calculate square root of positive real numbers\nComplex Mode: Calculate square root of complex numbers (a + bi)',
        },
        'ru': {
            'app_title': 'Калькулятор квадратного корня',
            'input_label': 'Входное значение:',
            'real_part_label': 'Действительная часть:',
            'imag_part_label': 'Мнимая часть:',
            'precision_label': 'Точность:',
            'precision_control': 'Управление точностью',
            'exact_value': 'Точное значение (1-1000):',
            'mode_label': 'Режим вычисления:',
            'mode_real': 'Действительные числа',
            'mode_complex': 'Комплексные числа',
            'calculate_button': 'Вычислить',
            'clear_button': 'Очистить',
            'result_label': 'Результат',
            'error_title': 'Ошибка',
            'invalid_input': 'Неверный ввод. Пожалуйста, введите корректное число.',
            'negative_real': 'Невозможно вычислить квадратный корень отрицательного действительного числа. Переключитесь в комплексный режим.',
            'invalid_precision': 'Точность должна быть положительным целым числом.',
            'calculation_error': 'Ошибка вычисления: {}',
            'language': 'Язык:',
            'language_menu': 'Язык',
            'english': 'English',
            'russian': 'Русский',
            'about': 'О программе',
            'about_text': 'Калькулятор квадратного корня v0.1.0\n\nМногофункциональный калькулятор для вычисления квадратных корней действительных и комплексных чисел с произвольной точностью.\n\nВозможности:\n- Поддержка действительных и комплексных чисел\n- Произвольная точность\n- Многоязычный интерфейс',
            'help': 'Справка',
            'help_text': 'Как использовать:\n\n1. Выберите режим вычисления (вкладка Действительные или Комплексные)\n2. Введите входное значение(я)\n3. Установите желаемую точность с помощью ползунка или поля ввода\n4. Нажмите Вычислить\n\nРежим действительных чисел: вычисление квадратного корня положительных действительных чисел\nРежим комплексных чисел: вычисление квадратного корня комплексных чисел (a + bi)',
        }
    }
    
    def __init__(self, language: str = 'en'):
        """
        Initialize translator with specified language.
        
        Args:
            language: Language code ('en' or 'ru')
        """
        self.language = language if language in self.TRANSLATIONS else 'en'
    
    def set_language(self, language: str):
        """Set the current language."""
        if language in self.TRANSLATIONS:
            self.language = language
    
    def get(self, key: str) -> str:
        """
        Get translated string for the current language.
        
        Args:
            key: Translation key
            
        Returns:
            Translated string or key if not found
        """
        return self.TRANSLATIONS.get(self.language, {}).get(key, key)
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages."""
        return {
            'en': self.TRANSLATIONS['en']['english'],
            'ru': self.TRANSLATIONS['ru']['russian']
        }
