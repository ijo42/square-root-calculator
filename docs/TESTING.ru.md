# Руководство по тестированию

> **[English version](TESTING.md)** | **Русская версия**

Комплексное руководство по запуску тестов в проекте Square Root Calculator.

## Быстрый старт

### Linux

```bash
# Сделать скрипт исполняемым
chmod +x run_tests.sh

# Запустить все тесты с покрытием
./run_tests.sh
```

### Windows

```cmd
# Запустить все тесты с покрытием
run_tests.bat
```

### Кроссплатформенно (Python скрипт)

```bash
# Работает на всех платформах
python run_tests.py
```

## Обзор тестовых скриптов

### 1. Полный набор тестов с покрытием

**`run_tests.sh` (Linux)** или **`run_tests.bat` (Windows)**

Возможности:
- Создаёт виртуальное окружение при необходимости
- Устанавливает все зависимости
- Запускает полный набор тестов
- Генерирует HTML отчёт о покрытии
- Генерирует XML отчёт о покрытии (для CI/CD)
- Показывает сводку покрытия в терминале
- Цветной вывод

Выходные файлы:
- `htmlcov/index.html` - Интерактивный HTML отчёт о покрытии
- `coverage.xml` - XML отчёт для CI инструментов
- `.coverage` - База данных покрытия

**Использование**:
```bash
# Linux
./run_tests.sh

# Windows
run_tests.bat
```

**Пример вывода**:
```
================================
Running Tests with Coverage
================================

Installing dependencies...
Done

Running tests...
============================= test session starts ==============================
collected 49 items

tests/test_calculator.py ................                               [ 32%]
tests/test_history.py ...........                                       [ 54%]
tests/test_translator.py .............                                  [ 80%]
tests/test_settings.py .........                                        [100%]

============================== 49 passed in 2.34s ==============================

Coverage Report:
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
src/square_root_calculator/core/calculator.py    95      2    98%
src/square_root_calculator/core/history.py       45      0   100%
src/square_root_calculator/core/settings.py      38      1    97%
src/square_root_calculator/locales/translator.py 52      0   100%
------------------------------------------------------------------
TOTAL                                            230      3    99%

HTML coverage report generated: htmlcov/index.html
```

### 2. Быстрые тесты (без покрытия)

**`test_quick.sh` (Linux)** или **`test_quick.bat` (Windows)**

Возможности:
- Быстрое выполнение тестов
- Без overhead покрытия
- Можно запускать конкретные тесты
- Идеально для итераций разработки

**Использование**:
```bash
# Все тесты
./test_quick.sh

# Конкретный файл
./test_quick.sh tests/test_calculator.py

# Конкретный тест
./test_quick.sh tests/test_calculator.py::test_simple_square_root
```

### 3. Кроссплатформенный скрипт

**`run_tests.py`**

Pure Python реализация, работает везде:
```bash
python run_tests.py
```

Возможности:
- Автоматическое определение окружения
- Установка зависимостей
- Генерация отчётов
- Работает на Windows, Linux

### 4. Makefile команды

Удобные shortcuts для общих задач:

```bash
# Тесты с покрытием
make test

# Быстрые тесты
make test-quick

# Открыть HTML отчёт
make coverage

# Запустить приложение
make run

# Проверки линтером
make lint

# Форматирование кода
make format

# Очистка сгенерированных файлов
make clean
```

## Ручное выполнение тестов

### Установка зависимостей

```bash
# С использованием pip
pip install -e ".[dev]"

# С использованием uv
uv sync
```

### Базовые pytest команды

```bash
# Запустить все тесты
pytest

# Verbose вывод
pytest -v

# Очень verbose (с выводом print)
pytest -vv -s

# Остановить на первой ошибке
pytest -x

# Показать 10 самых медленных тестов
pytest --durations=10
```

### Конкретные тесты

```bash
# Запустить файл
pytest tests/test_calculator.py

# Запустить класс
pytest tests/test_calculator.py::TestSquareRootCalculator

# Запустить конкретный тест
pytest tests/test_calculator.py::test_simple_square_root

# По паттерну имени
pytest -k "square_root"
```

### Тесты с покрытием

```bash
# Базовое покрытие
pytest --cov=src/square_root_calculator

# С отчётом в терминале
pytest --cov=src/square_root_calculator --cov-report=term

# С пропущенными строками
pytest --cov=src/square_root_calculator --cov-report=term-missing

# HTML отчёт
pytest --cov=src/square_root_calculator --cov-report=html

# XML отчёт (для CI)
pytest --cov=src/square_root_calculator --cov-report=xml

# Несколько форматов
pytest --cov=src/square_root_calculator --cov-report=html --cov-report=term
```

### Открытие HTML отчёта

```bash
# Linux
open htmlcov/index.html

# Windows
start htmlcov/index.html

# Или просто откройте в браузере
# file:///path/to/square-root-calculator/htmlcov/index.html
```

## Интерпретация отчётов о покрытии

### Терминальный отчёт

```
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
src/square_root_calculator/core/calculator.py    95      2    98%
src/square_root_calculator/core/history.py       45      0   100%
```

- **Stmts**: Всего исполняемых строк
- **Miss**: Пропущенные строки (не протестированные)
- **Cover**: Процент покрытия

### HTML отчёт

Откройте `htmlcov/index.html` в браузере:

1. **Overview page**: Сводка по всем файлам
2. **Цветовая индикация**:
   - Зелёный: Исполнено
   - Красный: Не исполнено
   - Серый: Исключено
3. **Кликните на файл**: Увидите построчное покрытие
4. **Номера строк**: Красные - не покрыты тестами

### Понимание метрик

**Целевые показатели**:
- 80%+ - Хорошо
- 90%+ - Отлично
- 95%+ - Превосходно
- 100% - Идеально (но не всегда достижимо)

**Важные модули** должны иметь 95%+ покрытие:
- `calculator.py` - Основная логика вычислений
- `translator.py` - Система локализации
- `history.py` - Управление историей
- `settings.py` - Управление настройками

## Структура тестов

### Организация тестовых файлов

```
tests/
├── conftest.py              # Фикстуры и конфигурация pytest
├── test_calculator.py       # Тесты калькулятора (16 тестов)
├── test_history.py          # Тесты истории (11 тестов)
├── test_translator.py       # Тесты переводов (13 тестов)
└── test_settings.py         # Тесты настроек (9 тестов)
```

### Соглашения об именовании

**Файлы**: `test_*.py` или `*_test.py`
**Функции**: `test_*`
**Классы**: `Test*`

**Примеры**:
```python
def test_simple_square_root():
    """Test simple square root calculation."""
    pass

class TestSquareRootCalculator:
    """Tests for SquareRootCalculator class."""
    
    def test_real_numbers(self):
        """Test real number calculations."""
        pass
```

### Тестовые категории

**test_calculator.py** (16 тестов):
- Perfect squares
- Irrational numbers
- Zero и один
- Отрицательные числа (ошибки)
- Комплексные числа
- Точность
- Валидация ввода
- Форматирование результата
- Множественные представления

**test_history.py** (11 тестов):
- Создание записей
- Добавление в историю
- Лимит записей
- Очистка истории
- Форматированный вывод
- Пустая история

**test_translator.py** (13 тестов):
- Английские переводы
- Русские переводы
- Смена языка
- Отсутствующие ключи
- Некорректный язык
- Новые функции

**test_settings.py** (9 тестов):
- Значения по умолчанию
- Get/set операции
- Отсутствующие ключи с default
- Сохранение настроек
- Сброс настроек

## Написание новых тестов

### Базовая структура теста

```python
import pytest
from square_root_calculator.core.calculator import SquareRootCalculator

def test_my_feature():
    """Test description."""
    # Arrange - подготовка
    calc = SquareRootCalculator(precision=10)
    input_value = "16"
    
    # Act - действие
    result = calc.sqrt_real(input_value)
    
    # Assert - проверка
    assert str(result) == "4.0000000000"
```

### Использование фикстур

```python
@pytest.fixture
def calculator():
    """Fixture providing calculator instance."""
    return SquareRootCalculator(precision=10)

def test_with_fixture(calculator):
    """Test using fixture."""
    result = calculator.sqrt_real("2")
    assert result > 0
```

### Параметризованные тесты

```python
@pytest.mark.parametrize("input_value,expected", [
    ("4", "2.0000000000"),
    ("9", "3.0000000000"),
    ("16", "4.0000000000"),
])
def test_perfect_squares(calculator, input_value, expected):
    """Test perfect square calculations."""
    result = calculator.sqrt_real(input_value)
    assert str(result) == expected
```

### Тестирование исключений

```python
def test_negative_raises_error():
    """Test that negative input raises error."""
    calc = SquareRootCalculator()
    
    with pytest.raises(InvalidInputError) as exc_info:
        calc.sqrt_real("-1")
    
    assert "negative" in str(exc_info.value).lower()
```

### Тестирование UI (PyQt)

```python
from pytestqt.qt_compat import qt_api

def test_button_click(qtbot):
    """Test button click behavior."""
    widget = MainWindow()
    qtbot.addWidget(widget)
    
    # Simulate click
    qtbot.mouseClick(widget.calculate_button, qt_api.QtCore.Qt.LeftButton)
    
    # Assert result
    assert widget.result_display.toPlainText() != ""
```

## CI/CD интеграция

### GitHub Actions

Проект использует GitHub Actions (`.github/workflows/ci.yml`):

**Test Job**:
```yaml
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest --cov=src/square_root_calculator --cov-report=xml --cov-report=html
```

**Lint Job**:
```yaml
- name: Lint with flake8
  run: flake8 src/ tests/
```

**Триггеры**:
- Pull requests в main/master
- Push в main/master

**Артефакты**:
- HTML coverage reports (30 дней)
- Загрузка в Codecov

### Локальная симуляция CI

```bash
# Запустить те же команды, что и CI
pip install -e ".[dev]"
pytest --cov=src/square_root_calculator --cov-report=xml
flake8 src/ tests/
black --check src/ tests/
```

### Pre-commit хуки

Создайте `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Run quick tests before commit
./test_quick.sh
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Сделайте исполняемым:
```bash
chmod +x .git/hooks/pre-commit
```

## Производительность тестов

### Измерение времени

```bash
# Показать 10 самых медленных тестов
pytest --durations=10

# Показать все длительности
pytest --durations=0
```

### Параллельное выполнение

```bash
# Установить pytest-xdist
pip install pytest-xdist

# Запустить с несколькими процессами
pytest -n auto  # Автоматическое определение
pytest -n 4     # 4 процесса
```

### Оптимизация медленных тестов

**Маркировка медленных тестов**:
```python
@pytest.mark.slow
def test_high_precision_calculation():
    """Slow test with 1000 digit precision."""
    pass
```

**Пропуск медленных тестов**:
```bash
# Запустить только быстрые тесты
pytest -m "not slow"

# Запустить только медленные
pytest -m slow
```

## Устранение неполадок

### Проблема: Тесты не найдены

**Причина**: pytest не находит тесты

**Решение**:
```bash
# Проверьте структуру
pytest --collect-only

# Убедитесь, что в пути
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Или установите в editable режиме
pip install -e .
```

### Проблема: Import errors

**Причина**: Модули не найдены

**Решение**:
```bash
# Установите зависимости
pip install -e ".[dev]"

# Или с uv
uv sync
```

### Проблема: Coverage не генерируется

**Причина**: Неправильные пути

**Решение**:
```bash
# Укажите правильный source
pytest --cov=src/square_root_calculator

# Проверьте .coveragerc или pytest.ini
cat pytest.ini
```

### Проблема: Тесты UI падают

**Причина**: Нет display для PyQt

**Решение** (Linux):
```bash
# Установите xvfb
sudo apt-get install xvfb

# Запустите с виртуальным display
xvfb-run pytest
```

### Проблема: Медленные тесты

**Причина**: Высокая точность или много тестов

**Решение**:
```bash
# Используйте быстрые тесты
./test_quick.sh

# Или параллельное выполнение
pytest -n auto
```

## Лучшие практики

### 1. Изолируйте тесты

Каждый тест должен быть независимым:
```python
def test_isolated():
    """Each test starts fresh."""
    calc = SquareRootCalculator()  # Новый экземпляр
    # Test code
```

### 2. Используйте понятные имена

```python
# Хорошо
def test_sqrt_of_negative_number_raises_error():
    pass

# Плохо
def test_1():
    pass
```

### 3. Один assert на тест (когда возможно)

```python
# Хорошо
def test_result_is_positive():
    result = calculate(4)
    assert result > 0

def test_result_is_correct():
    result = calculate(4)
    assert result == 2

# Приемлемо для связанных проверок
def test_calculation_result():
    result = calculate(4)
    assert result == 2
    assert isinstance(result, Decimal)
```

### 4. Используйте фикстуры для setup

```python
@pytest.fixture
def temp_settings(tmp_path):
    """Fixture with temporary settings."""
    settings_file = tmp_path / "settings.json"
    return Settings(str(settings_file))
```

### 5. Тестируйте edge cases

```python
def test_edge_cases():
    """Test boundary conditions."""
    calc = SquareRootCalculator()
    
    # Zero
    assert calc.sqrt_real("0") == 0
    
    # Very small
    result = calc.sqrt_real("0.0000001")
    assert result > 0
    
    # Very large
    result = calc.sqrt_real("999999999999")
    assert result > 0
```

### 6. Документируйте тесты

```python
def test_complex_behavior():
    """
    Test complex number calculation.
    
    Given: Complex number 3+4i
    When: Calculate square root
    Then: Result should be 2+1i
    """
    pass
```

## Полезные ресурсы

### Документация

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pytest-qt Documentation](https://pytest-qt.readthedocs.io/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

### Инструменты

- **pytest**: Test framework
- **pytest-cov**: Coverage plugin
- **pytest-qt**: PyQt testing support
- **pytest-xdist**: Parallel execution
- **coverage**: Coverage measurement

### Команды быстрого доступа

```bash
# Основные
pytest                              # Все тесты
pytest -v                           # Verbose
pytest --cov                        # С покрытием
make test                           # Полный набор

# Специфичные
pytest tests/test_calculator.py    # Один файл
pytest -k "test_square"             # По имени
pytest -x                           # Стоп на ошибке
pytest --lf                         # Только последние failed

# Отчёты
pytest --cov-report=html            # HTML отчёт
pytest --durations=10               # Медленные тесты
pytest --collect-only               # Список тестов
```

## Заключение

Тестирование - критическая часть разработки качественного ПО. Этот проект включает:

- **49 тестов** для всех основных компонентов
- **Множество скриптов** для удобного запуска
- **Автоматизированное CI/CD** с GitHub Actions
- **Отчёты о покрытии** для отслеживания качества

Всегда запускайте тесты перед:
- Созданием pull request
- Коммитом важных изменений
- Релизом новой версии

---

**[🔝 Наверх](#руководство-по-тестированию)** | **[English version](TESTING.md)**
