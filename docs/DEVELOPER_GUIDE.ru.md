# Руководство разработчика

> **[English version](DEVELOPER_GUIDE.md)** | **Русская версия**

Техническая документация для разработчиков Square Root Calculator.

## Содержание

- [Архитектура](#архитектура)
- [Модули](#модули)
- [API Reference](#api-reference)
- [Дизайн UI](#дизайн-ui)
- [Локализация](#локализация)
- [Расширение функциональности](#расширение-функциональности)

## Архитектура

### Обзор системы

```
┌─────────────────────────────────────────────────────────┐
│                    Main Application                      │
│                     (main.py)                            │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
┌────────▼─────────┐        ┌────────▼─────────┐
│   UI Layer       │        │   Core Layer     │
│  (main_window)   │◄───────┤   (calculator)   │
└────────┬─────────┘        └────────┬─────────┘
         │                            │
         │                   ┌────────┴─────────┐
    ┌────▼────┐         ┌───▼───┐      ┌──────▼──────┐
    │Translator│         │History│      │Settings     │
    └─────────┘         └───────┘      └─────────────┘
```

### Паттерны проектирования

**1. MVC Pattern**:
- **Model**: Core modules (calculator, history, settings)
- **View**: UI module (main_window)
- **Controller**: Event handlers в main_window

**2. Singleton Pattern**:
- Settings: Единственный экземпляр настроек
- Translator: Один экземпляр для всего приложения

**3. Observer Pattern**:
- UI обновляется при изменении настроек
- История обновляет display при добавлении записей

## Модули

### Core Layer

#### calculator.py

**Назначение**: Вычисление квадратных корней с произвольной точностью

**Классы**:

```python
class CalculationResult:
    """
    Контейнер для результатов вычислений.
    
    Attributes:
        input_value: Входное значение (str)
        positive_root: Положительный корень (Decimal или complex)
        negative_root: Отрицательный корень (Decimal или complex)
        decimal_repr: Десятичное представление (str)
        scientific_repr: Научная нотация (str)
        fractional_repr: Дробное представление (str)
        polar_repr: Полярная форма для комплексных (str)
        exponential_repr: Экспоненциальная форма (str)
    """
```

```python
class SquareRootCalculator:
    """
    Калькулятор квадратного корня с произвольной точностью.
    
    Args:
        precision (int): Точность вычислений (1-1000)
        
    Methods:
        calculate(real_value, real_part, imag_part): Универсальный метод
        sqrt_real(value): Квадратный корень действительного числа
        sqrt_complex(real, imag): Квадратный корень комплексного числа
        format_result(result): Форматирование результата
    """
```

**Алгоритмы**:

*Действительные числа*:
```python
def sqrt_real(self, value: str) -> Decimal:
    """
    Использует Decimal.sqrt() для точного вычисления.
    
    Formula: √x где x ≥ 0
    
    Precision: Настраивается через getcontext().prec
    """
    decimal_value = Decimal(value)
    if decimal_value < 0:
        raise InvalidInputError("Cannot calculate sqrt of negative")
    return decimal_value.sqrt()
```

*Комплексные числа*:
```python
def sqrt_complex(self, a: float, b: float) -> Tuple[Decimal, Decimal]:
    """
    Использует математическую формулу для √(a + bi).
    
    Formula:
        r = √(a² + b²)  (модуль)
        real = √((r + a) / 2)
        imag = sign(b) × √((r - a) / 2)
        
    Returns:
        (real_part, imaginary_part)
    """
```

#### history.py

**Назначение**: Управление историей вычислений

**Классы**:

```python
class HistoryEntry:
    """
    Запись истории.
    
    Attributes:
        input_value: Входные данные
        result: Результат вычисления
        timestamp: Время вычисления (datetime)
    """

class HistoryManager:
    """
    Менеджер истории вычислений.
    
    Attributes:
        max_entries: Максимум записей (по умолчанию 50)
        entries: Список HistoryEntry
        
    Methods:
        add_entry(input_val, result): Добавить запись
        clear(): Очистить историю
        get_formatted_history(): Форматированный вывод
    """
```

**Хранение**:
- В памяти (список entries)
- Не персистентно (сбрасывается при закрытии)
- FIFO при достижении лимита

#### settings.py

**Назначение**: Управление постоянными настройками

**Класс**:

```python
class Settings:
    """
    Менеджер настроек приложения.
    
    Настройки хранятся в: ~/.square_root_calculator/settings.json
    
    Default values:
        precision: 4
        theme: 'light'
        language: 'en'
        show_exact_precision: False
        show_negative_roots: True
        
    Methods:
        get(key, default): Получить значение
        set(key, value): Установить значение
        reset(): Сбросить к defaults
    """
```

**Формат файла**:
```json
{
    "precision": 4,
    "theme": "light",
    "language": "en",
    "show_exact_precision": false,
    "show_negative_roots": true
}
```

#### update_checker.py

**Назначение**: Проверка обновлений из GitHub

**Класс**:

```python
class UpdateChecker:
    """
    Проверяет версию в master ветке GitHub.
    
    Args:
        owner: Владелец репозитория
        repo: Название репозитория
        current_version: Текущая версия
        
    Methods:
        check_for_updates(): Проверить обновления
            Returns: (has_update, latest_version, error_message)
    """
```

**Процесс**:
1. Fetch `pyproject.toml` из master ветки
2. Парсинг версии из `[project] version = "..."`
3. Сравнение с текущей версией
4. Возврат результата

### UI Layer

#### main_window.py

**Назначение**: Главное окно приложения PyQt6

**Класс**:

```python
class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    
    Components:
        - Mode tabs (Real/Complex)
        - Input fields
        - Precision controls (slider + spinbox)
        - Calculate/Clear buttons
        - Result display
        - History panel
        - Menu bar (Language, Settings, Help)
        
    Signals:
        - Кнопки: clicked
        - Слайдер: valueChanged
        - История: itemClicked
    """
```

**Методы**:

```python
def calculate(self):
    """Обработчик кнопки Calculate."""
    # 1. Получить входные данные
    # 2. Определить режим (Real/Complex)
    # 3. Вызвать calculator
    # 4. Отобразить результат
    # 5. Добавить в историю

def display_result(self, result: CalculationResult):
    """
    Отобразить результат в унифицированном формате.
    
    HTML форматирование с секциями:
    - Input Value
    - Square Roots (positive + negative)
    - Representations (decimal, scientific, fractional)
    - Alternative Forms (для комплексных)
    """

def apply_theme(self, theme: str):
    """
    Применить тему оформления.
    
    Args:
        theme: 'light' или 'dark'
        
    Uses: qt_material library
    """
```

### Localization Layer

#### translator.py

**Назначение**: Система многоязычности

**Класс**:

```python
class Translator:
    """
    Менеджер переводов.
    
    Supported languages: 'en', 'ru'
    
    Storage: Словари в памяти
    
    Methods:
        get(key): Получить перевод
        set_language(lang): Сменить язык
    """
```

**Структура переводов**:

```python
translations = {
    'en': {
        'app_title': 'Square Root Calculator',
        'calculate': 'Calculate',
        'clear': 'Clear',
        # ... более 50 ключей
    },
    'ru': {
        'app_title': 'Калькулятор квадратного корня',
        'calculate': 'Вычислить',
        'clear': 'Очистить',
        # ... более 50 ключей
    }
}
```

**Добавление нового языка**:

1. Добавить словарь в `translations`
2. Перевести все ключи
3. Добавить в Language меню
4. Тестировать UI

## API Reference

### Calculator API

```python
from square_root_calculator.core.calculator import SquareRootCalculator

# Создать калькулятор
calc = SquareRootCalculator(precision=10)

# Действительные числа
result = calc.sqrt_real("2")
print(result)  # 1.4142135624

# Комплексные числа
real, imag = calc.sqrt_complex(3, 4)
print(f"{real} + {imag}i")  # 2.0 + 1.0i

# Универсальный метод
result = calc.calculate(real_value="2")  # Действительное
result = calc.calculate(real_part=3, imag_part=4)  # Комплексное
```

### History API

```python
from square_root_calculator.core.history import HistoryManager

# Создать менеджер
history = HistoryManager(max_entries=50)

# Добавить запись
history.add_entry("2", "1.414...")

# Получить историю
entries = history.get_formatted_history()

# Очистить
history.clear()
```

### Settings API

```python
from square_root_calculator.core.settings import Settings

# Получить настройки
settings = Settings()

# Чтение
precision = settings.get('precision', default=4)

# Запись (автосохранение)
settings.set('theme', 'dark')

# Сброс
settings.reset()
```

### Translator API

```python
from square_root_calculator.locales.translator import Translator

# Создать translator
t = Translator('en')

# Получить перевод
title = t.get('app_title')

# Сменить язык
t.set_language('ru')
title = t.get('app_title')  # "Калькулятор квадратного корня"
```

## Дизайн UI

### Компоненты

**Layout Structure**:
```
QMainWindow
├── MenuBar
│   ├── Language Menu
│   ├── Settings Menu
│   └── Help Menu
├── Central Widget (QWidget)
│   ├── Mode Tabs (QTabWidget)
│   │   ├── Real Numbers Tab
│   │   │   └── Input Field (QLineEdit)
│   │   └── Complex Numbers Tab
│   │       ├── Real Part (QLineEdit)
│   │       └── Imaginary Part (QLineEdit)
│   ├── Precision Group (QGroupBox)
│   │   ├── Precision Label
│   │   ├── Slider (QSlider) [1-200]
│   │   └── Spinbox (QSpinBox) [1-1000] (optional)
│   ├── Buttons (QHBoxLayout)
│   │   ├── Calculate (QPushButton)
│   │   └── Clear (QPushButton)
│   └── Splitter (QSplitter)
│       ├── Result Display (QTextEdit)
│       └── History Panel (QListWidget)
```

### Темы

**Light Theme** (по умолчанию):
- Светлый фон
- Тёмный текст
- Синие акценты

**Dark Theme**:
- Тёмный фон (#1e1e1e)
- Светлый текст
- Голубые акценты

**Применение темы**:
```python
from qt_material import apply_stylesheet

# Светлая
apply_stylesheet(app, theme='light_blue.xml')

# Тёмная
apply_stylesheet(app, theme='dark_blue.xml')
```

### Стилизация

**Custom Styles**:
```python
# Primary button
calculate_button.setStyleSheet("""
    QPushButton {
        background-color: #0066cc;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #0052a3;
    }
""")

# Result display
result_display.setStyleSheet("""
    QTextEdit {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        padding: 10px;
    }
""")
```

## Локализация

### Добавление нового перевода

1. **Обновить translator.py**:
```python
translations = {
    'en': { ... },
    'ru': { ... },
    'de': {  # Новый язык
        'app_title': 'Quadratwurzel-Rechner',
        'calculate': 'Berechnen',
        # ... все ключи
    }
}
```

2. **Обновить Language меню**:
```python
german_action = QAction('Deutsch', self)
german_action.triggered.connect(lambda: self.change_language('de'))
language_menu.addAction(german_action)
```

3. **Тестировать**:
```bash
pytest tests/test_translator.py
```

### Ключи переводов

Категории ключей:
- **UI labels**: `input_value`, `precision`, `calculate`
- **Modes**: `real_numbers`, `complex_numbers`
- **Results**: `positive_root`, `negative_root`, `representations`
- **Menus**: `language`, `settings`, `help`
- **Messages**: `error`, `success`, `update_available`

## Расширение функциональности

### Добавление нового режима

1. **Создать новую вкладку**:
```python
new_tab = QWidget()
# Add input fields
self.mode_tabs.addTab(new_tab, "New Mode")
```

2. **Добавить логику**:
```python
def calculate_new_mode(self):
    # Get input
    # Calculate
    # Display result
    pass
```

3. **Обновить calculate()**:
```python
if self.mode_tabs.currentIndex() == 2:  # New mode
    self.calculate_new_mode()
```

### Добавление новых представлений

1. **Обновить CalculationResult**:
```python
@dataclass
class CalculationResult:
    # ... existing fields
    new_representation: str = ""
```

2. **Вычислить представление**:
```python
def calculate_new_repr(value):
    # Logic here
    return formatted_string
```

3. **Добавить в display**:
```python
def display_result(self, result):
    # ... existing code
    output += f"<p>New Representation: {result.new_representation}</p>"
```

### Добавление настроек

1. **Обновить defaults в Settings**:
```python
self.defaults = {
    # ... existing
    'new_setting': default_value
}
```

2. **Добавить в Settings меню**:
```python
new_action = QAction('New Setting', self)
new_action.setCheckable(True)
new_action.triggered.connect(self.toggle_new_setting)
settings_menu.addAction(new_action)
```

3. **Использовать**:
```python
if self.settings.get('new_setting', False):
    # Apply setting
```

## Debugging

### Логирование

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Calculating sqrt of {value}")
logger.error(f"Error occurred: {e}")
```

### PyQt Debugging

```python
# Enable Qt debug messages
import sys
sys.excepthook = lambda *args: print(args)

# Print widget hierarchy
def print_widget_tree(widget, level=0):
    print("  " * level + widget.__class__.__name__)
    for child in widget.children():
        print_widget_tree(child, level + 1)
```

### Profiling

```bash
# Profile application
python -m cProfile -o profile.stats main.py

# View results
python -m pstats profile.stats
> sort cumtime
> stats 10
```

## Заключение

Этот проект демонстрирует:
- Чистую архитектуру с разделением слоёв
- Современные практики Python разработки
- Кроссплатформенный UI с PyQt6
- Комплексное тестирование
- Хорошую документацию

Для дополнительной информации см.:
- [Руководство по тестированию](TESTING.ru.md)
- [Примеры использования](USAGE_EXAMPLES.ru.md)

---

**[🔝 Наверх](#руководство-разработчика)** | **[English version](DEVELOPER_GUIDE.md)**
