"""Localization system for multilingual support.

Система локализации для поддержки нескольких языков.
"""

import json
from pathlib import Path
from typing import Dict


class Translator:
    """Simple translation system supporting multiple languages.

    Простая система перевода с поддержкой нескольких языков.
    """

    TRANSLATIONS: Dict[str, Dict[str, str]] = {
        "en": {
            "app_title": "Square Root Calculator",
            "input_label": "Input Value:",
            "real_part_label": "Real Part:",
            "imag_part_label": "Imaginary Part:",
            "precision_label": "Precision:",
            "precision_control": "Precision Control",
            "exact_value": "Exact value (1-1000):",
            "mode_label": "Calculation Mode:",
            "mode_real": "Real Numbers",
            "mode_complex": "Complex Numbers",
            "calculate_button": "Calculate",
            "clear_button": "Clear",
            "clear_history_button": "Clear History",
            "result_label": "Result",
            "roots_label": "Square Roots:",
            "root_positive": "Positive root:",
            "root_negative": "Negative root:",
            "representations_label": "Representations:",
            "decimal_repr": "Decimal:",
            "scientific_repr": "Scientific:",
            "fraction_repr": "Fraction:",
            "history_label": "Calculation History",
            "history_empty": "No calculation history",
            "error_title": "Error",
            "invalid_input": "Invalid input. Please enter a valid number.",
            "text_instead_of_numbers": "Text characters are not allowed in number input",
            "negative_real": "Cannot calculate square root of negative real number. Switch to Complex mode.",
            "invalid_precision": "Precision must be a positive integer.",
            "calculation_error": "Calculation error: {}",
            "precision_too_low": "Precision too low for this calculation. Please increase precision to at least {} decimal places.",
            "precision_error_generic": "Calculation error with current precision ({}). Please increase precision to at least {} decimal places for this calculation.",
            "language": "Language:",
            "language_menu": "Language",
            "english": "English",
            "russian": "Русский",
            "about": "About",
            "about_text": "Square Root Calculator v{}\n\nA comprehensive calculator for computing square roots of real and complex numbers with arbitrary precision.\n\nFeatures:\n- Real and complex number support\n- Arbitrary precision\n- Multilingual interface\n- Calculation history\n- Automatic update checking",
            "help": "Help",
            "help_text": "How to use:\n\n1. Choose calculation mode (Real or Complex tab)\n2. Enter the input value(s)\n3. Set desired precision using slider or spinbox\n4. Click Calculate\n\nReal Mode: Calculate square root of positive real numbers\nComplex Mode: Calculate square root of complex numbers (a + bi)\n\nThe calculator displays both positive and negative roots, multiple number representations, and maintains a history of calculations.",
            "update_available": "Update Available",
            "update_message": "Version {} is available!\nCurrent version: {}\n\nClick OK to open the download page.",
            "update_check_failed": "Could not check for updates",
            "no_update": "You are using the latest version",
            "check_updates": "Check for Updates",
            "download_url": "https://github.com/ijo42/square-root-calculator/releases",
            "skip_update": "Skip",
            "download_update": "Download",
            "reload_translations": "Reload Translations",
            "translations_reloaded": "Translations have been reloaded successfully!",
            "settings": "Settings",
            "theme": "Theme",
            "theme_light": "Light Theme",
            "theme_dark": "Dark Theme",
            "show_exact_precision": "Show Exact Precision Field",
            "show_negative_roots": "Show Negative Roots",
            "user_manual": "User Manual",
            "polar_form": "Polar form:",
            "exponential_form": "Exponential form:",
            "alternative_forms": "Alternative Forms:",
        },
        "ru": {
            "app_title": "Калькулятор квадратного корня",
            "input_label": "Входное значение:",
            "real_part_label": "Действительная часть:",
            "imag_part_label": "Мнимая часть:",
            "precision_label": "Точность:",
            "precision_control": "Управление точностью",
            "exact_value": "Точное значение (1-1000):",
            "mode_label": "Режим вычисления:",
            "mode_real": "Действительные числа",
            "mode_complex": "Комплексные числа",
            "calculate_button": "Вычислить",
            "clear_button": "Очистить",
            "clear_history_button": "Очистить историю",
            "result_label": "Результат",
            "roots_label": "Квадратные корни:",
            "root_positive": "Положительный корень:",
            "root_negative": "Отрицательный корень:",
            "representations_label": "Представления:",
            "decimal_repr": "Десятичное:",
            "scientific_repr": "Научное:",
            "fraction_repr": "Дробь:",
            "history_label": "История вычислений",
            "history_empty": "История вычислений пуста",
            "error_title": "Ошибка",
            "invalid_input": "Неверный ввод. Пожалуйста, введите корректное число.",
            "text_instead_of_numbers": "Текстовые символы не допускаются в числовом вводе",
            "negative_real": "Невозможно вычислить квадратный корень отрицательного действительного числа. Переключитесь в комплексный режим.",
            "invalid_precision": "Точность должна быть положительным целым числом.",
            "calculation_error": "Ошибка вычисления: {}",
            "precision_too_low": "Точность слишком низкая для данного вычисления. Пожалуйста, увеличьте точность минимум до {} знаков после запятой.",
            "precision_error_generic": "Ошибка вычисления с текущей точностью ({}). Пожалуйста, увеличьте точность минимум до {} знаков после запятой для данного вычисления.",
            "language": "Язык:",
            "language_menu": "Язык",
            "english": "English",
            "russian": "Русский",
            "about": "О программе",
            "about_text": "Калькулятор квадратного корня v{}\n\nМногофункциональный калькулятор для вычисления квадратных корней действительных и комплексных чисел с произвольной точностью.\n\nВозможности:\n- Поддержка действительных и комплексных чисел\n- Произвольная точность\n- Многоязычный интерфейс\n- История вычислений\n- Автоматическая проверка обновлений",
            "help": "Справка",
            "help_text": "Как использовать:\n\n1. Выберите режим вычисления (вкладка Действительные или Комплексные)\n2. Введите входное значение(я)\n3. Установите желаемую точность с помощью ползунка или поля ввода\n4. Нажмите Вычислить\n\nРежим действительных чисел: вычисление квадратного корня положительных действительных чисел\nРежим комплексных чисел: вычисление квадратного корня комплексных чисел (a + bi)\n\nКалькулятор отображает положительный и отрицательный корни, различные представления чисел и ведет историю вычислений.",
            "update_available": "Доступно обновление",
            "update_message": "Доступна версия {}!\nТекущая версия: {}\n\nНажмите OK, чтобы открыть страницу загрузки.",
            "update_check_failed": "Не удалось проверить обновления",
            "no_update": "Вы используете последнюю версию",
            "check_updates": "Проверить обновления",
            "download_url": "https://github.com/ijo42/square-root-calculator/releases",
            "skip_update": "Пропустить",
            "download_update": "Скачать",
            "reload_translations": "Обновить переводы",
            "translations_reloaded": "Переводы успешно обновлены!",
            "settings": "Настройки",
            "theme": "Тема",
            "theme_light": "Светлая тема",
            "theme_dark": "Тёмная тема",
            "show_exact_precision": "Показать поле точного значения",
            "show_negative_roots": "Показать отрицательные корни",
            "user_manual": "Руководство пользователя",
            "polar_form": "Полярная форма:",
            "exponential_form": "Экспоненциальная форма:",
            "alternative_forms": "Альтернативные формы:",
        },
    }

    def __init__(self, language: str = "en"):
        """Initialize translator with specified language.

        Инициализировать переводчик с указанным языком.

        Args:
            language: Language code ('en' or 'ru')
                     Код языка ('en' или 'ru')
        """
        self.language = language if language in self.TRANSLATIONS else "en"
        self.custom_translations_loaded = False
        self.load_custom_translations()

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
                        try:
                            with open(json_file, 'r', encoding='utf-8') as f:
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
        # Reset to built-in translations first
        self.__init__(self.language)

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

    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages.

        Получить список доступных языков.

        Returns:
            Dictionary mapping language codes to names
            Словарь, сопоставляющий коды языков с названиями
        """
        return {
            "en": self.TRANSLATIONS["en"]["english"],
            "ru": self.TRANSLATIONS["ru"]["russian"],
        }
