# Руководство по внесению вклада

> **[English version](CONTRIBUTING.md)** | **Русская версия**

Спасибо за ваш интерес к проекту Square Root Calculator! Этот документ содержит рекомендации по внесению вклада в проект.

## Содержание

- [Кодекс поведения](#кодекс-поведения)
- [Как внести вклад](#как-внести-вклад)
- [Настройка среды разработки](#настройка-среды-разработки)
- [Процесс разработки](#процесс-разработки)
- [Стандарты кода](#стандарты-кода)
- [Тестирование](#тестирование)
- [Документация](#документация)
- [Процесс pull request](#процесс-pull-request)

## Кодекс поведения

### Наши обязательства

Мы как участники и сопровождающие проекта обязуемся сделать участие в нашем проекте и сообществе свободным от притеснений опытом для всех.

### Наши стандарты

Примеры поведения, которое способствует созданию позитивной среды:
- Использование доброжелательного и инклюзивного языка
- Уважение различных точек зрения и опыта
- Принятие конструктивной критики
- Фокус на том, что лучше для сообщества
- Проявление эмпатии к другим участникам

## Как внести вклад

### Сообщение об ошибках

Перед созданием отчёта об ошибке:
1. Проверьте существующие issues
2. Убедитесь, что используете последнюю версию
3. Соберите информацию о проблеме

**Хороший отчёт об ошибке содержит**:
- Чёткое и описательное название
- Точные шаги для воспроизведения
- Ожидаемое поведение
- Фактическое поведение
- Скриншоты (если применимо)
- Версию Python и ОС
- Полный traceback ошибки

### Предложение улучшений

**Перед предложением улучшения**:
- Проверьте, не было ли уже такого предложения
- Убедитесь, что оно соответствует целям проекта

**Хорошее предложение улучшения содержит**:
- Чёткое и описательное название
- Подробное описание предложенной функциональности
- Объяснение, почему это улучшение полезно
- Возможные альтернативные решения

### Pull Requests

Мы приветствуем pull requests!  Для больших изменений сначала откройте issue для обсуждения.

## Настройка среды разработки

### Предварительные требования

- Python 3.12 или выше
- pip или uv для управления пакетами
- Git

### Шаги установки

1. **Форкните репозиторий**
   ```bash
   # На GitHub нажмите кнопку "Fork"
   ```

2. **Клонируйте свой форк**
   ```bash
   git clone https://github.com/YOUR-USERNAME/square-root-calculator.git
   cd square-root-calculator
   ```

3. **Добавьте upstream remote**
   ```bash
   git remote add upstream https://github.com/ijo42/square-root-calculator.git
   ```

4. **Установите зависимости**
   ```bash
   # С использованием pip
   pip install -e ".[dev]"
   
   # Или с использованием uv
   uv sync
   ```

5. **Проверьте установку**
   ```bash
   # Запустите тесты
   pytest
   
   # Запустите приложение
   python main.py
   ```

### Структура проекта

```
square-root-calculator/
├── src/square_root_calculator/    # Основной код приложения
│   ├── core/                      # Базовая функциональность
│   │   ├── calculator.py          # Движок вычислений
│   │   ├── history.py             # Управление историей
│   │   ├── settings.py            # Настройки
│   │   └── update_checker.py      # Проверка обновлений
│   ├── ui/                        # Пользовательский интерфейс
│   │   └── main_window.py         # Главное окно
│   └── locales/                   # Локализация
│       └── translator.py          # Переводы
├── tests/                         # Тестовый набор
│   ├── test_calculator.py         # Тесты калькулятора
│   ├── test_history.py            # Тесты истории
│   ├── test_translator.py         # Тесты переводов
│   └── test_settings.py           # Тесты настроек
├── docs/                          # Документация
├── .github/workflows/             # GitHub Actions
└── main.py                        # Точка входа
```

## Процесс разработки

### Рабочий процесс с Git

1. **Создайте ветку для работы**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Внесите изменения**
   ```bash
   # Редактируйте файлы
   # Тестируйте изменения
   ```

3. **Зафиксируйте изменения**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

4. **Синхронизируйтесь с upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Отправьте изменения**
   ```bash
   git push origin feature/amazing-feature
   ```

### Соглашения о ветвях

- `main` - стабильная ветка
- `feature/*` - новая функциональность
- `bugfix/*` - исправления ошибок
- `docs/*` - изменения документации
- `refactor/*` - рефакторинг кода

### Соглашения о коммитах

Используйте чёткие и описательные сообщения коммитов:

```
Тип: Краткое описание (не более 50 символов)

Подробное описание того, что и почему изменено (если нужно).
Разбивайте на строки по 72 символа.

Связанные issue: #123
```

**Типы коммитов**:
- `feat`: Новая функциональность
- `fix`: Исправление ошибки
- `docs`: Изменения документации
- `style`: Форматирование, отсутствующие точки с запятой и т.д.
- `refactor`: Рефакторинг кода
- `test`: Добавление тестов
- `chore`: Обновление задач сборки, конфигурации и т.д.

**Примеры**:
```
feat: Add dark theme support

Implements dark theme using qt-material library.
Users can switch themes via Settings menu.

Related issue: #42
```

```
fix: Correct complex number calculation

Fixed sign error in imaginary part calculation.
Added test case to prevent regression.

Fixes #38
```

## Стандарты кода

### Стиль Python

Мы следуем [PEP 8](https://www.python.org/dev/peps/pep-0008/) с небольшими исключениями:
- Максимальная длина строки: 100 символов
- Используйте 4 пробела для отступов

### Форматирование

Используйте **black** для автоматического форматирования:
```bash
# Форматировать все файлы
black src/ tests/

# Проверить без изменений
black --check src/ tests/
```

### Линтинг

Используйте **flake8** для проверки кода:
```bash
# Проверить код
flake8 src/ tests/

# С конфигурацией из setup.cfg
flake8
```

### Аннотации типов

Используйте аннотации типов для функций и методов:
```python
from decimal import Decimal
from typing import Tuple, Optional

def calculate_root(value: Decimal, precision: int) -> Tuple[Decimal, Decimal]:
    """
    Calculate square root with given precision.
    
    Args:
        value: Input value
        precision: Number of decimal places
        
    Returns:
        Tuple of (positive_root, negative_root)
    """
    pass
```

### Docstrings

Используйте Google style docstrings:
```python
def complex_function(param1: int, param2: str) -> bool:
    """
    Short description of function.
    
    Longer description if needed, explaining what the function does
    and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is negative
        TypeError: When param2 is not a string
        
    Example:
        >>> complex_function(5, "test")
        True
    """
    pass
```

### Именование

- **Классы**: `PascalCase` (например, `SquareRootCalculator`)
- **Функции/методы**: `snake_case` (например, `calculate_square_root`)
- **Константы**: `UPPER_SNAKE_CASE` (например, `MAX_PRECISION`)
- **Приватные**: начинаются с `_` (например, `_internal_method`)

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/test_calculator.py

# С покрытием
pytest --cov=src/square_root_calculator

# С HTML отчётом
pytest --cov=src/square_root_calculator --cov-report=html
```

### Использование скриптов

```bash
# Linux/macOS
./run_tests.sh

# Windows
run_tests.bat

# Кроссплатформенно
python run_tests.py

# Быстрые тесты
./test_quick.sh
```

### Написание тестов

**Структура теста**:
```python
import pytest
from square_root_calculator.core.calculator import SquareRootCalculator

def test_simple_square_root():
    """Test simple square root calculation."""
    # Arrange
    calc = SquareRootCalculator(precision=10)
    
    # Act
    result = calc.sqrt_real("4")
    
    # Assert
    assert str(result) == "2.0000000000"

def test_negative_input_raises_error():
    """Test that negative input raises InvalidInputError."""
    calc = SquareRootCalculator()
    
    with pytest.raises(InvalidInputError):
        calc.sqrt_real("-1")
```

**Фикстуры**:
```python
@pytest.fixture
def calculator():
    """Fixture for calculator instance."""
    return SquareRootCalculator(precision=10)

def test_with_fixture(calculator):
    """Test using fixture."""
    result = calculator.sqrt_real("2")
    assert result > 0
```

### Требования к покрытию

- Минимум 80% покрытия для нового кода
- 100% покрытия для критических модулей
- Все исправления ошибок должны включать тест

## Документация

### Обновление документации

При добавлении новой функциональности обновите:
1. **README.md** - если меняется основная функциональность
2. **docs/USAGE_EXAMPLES.md** - добавьте примеры использования
3. **docs/DEVELOPER_GUIDE.md** - если меняется API
4. **Docstrings** - в коде

### Форматирование документации

- Используйте Markdown
- Добавляйте примеры кода с синтаксической подсветкой
- Включайте скриншоты для UI изменений
- Обновляйте оглавление

### Bilingual Documentation

Для документации пользователя:
- Поддерживайте английскую и русскую версии
- Файлы: `*.md` (English) и `*.ru.md` (Russian)
- Обновляйте обе версии одновременно

## Процесс Pull Request

### Перед созданием PR

**Чеклист**:
- [ ] Код соответствует стандартам стиля
- [ ] Все тесты проходят
- [ ] Добавлены тесты для нового кода
- [ ] Документация обновлена
- [ ] Коммиты имеют понятные сообщения
- [ ] Ветка синхронизирована с main

### Создание PR

1. **Откройте Pull Request на GitHub**
2. **Заполните шаблон PR**:
   ```markdown
   ## Описание
   Краткое описание изменений
   
   ## Тип изменения
   - [ ] Исправление ошибки
   - [ ] Новая функциональность
   - [ ] Критическое изменение
   - [ ] Документация
   
   ## Как протестировано
   Описание тестирования
   
   ## Чеклист
   - [ ] Тесты проходят локально
   - [ ] Lint проверки проходят
   - [ ] Документация обновлена
   ```

3. **Свяжите related issues**:
   ```
   Closes #123
   Fixes #456
   Related to #789
   ```

### Процесс review

1. **Автоматические проверки**:
   - GitHub Actions запускает тесты
   - Lint проверки
   - Coverage отчёты

2. **Code review**:
   - Мейнтейнер просматривает код
   - Может запросить изменения
   - Обсуждение в комментариях

3. **Адресация feedback**:
   ```bash
   # Внесите изменения
   git add .
   git commit -m "Address review feedback"
   git push origin feature/amazing-feature
   ```

4. **Merge**:
   - После одобрения мейнтейнер сольёт PR
   - Используется squash merge для чистой истории

## Полезные команды

### Команды Make

```bash
make test          # Запустить все тесты с покрытием
make test-quick    # Быстрые тесты
make coverage      # Открыть HTML отчёт
make lint          # Запустить линтер
make format        # Форматировать код
make run           # Запустить приложение
make clean         # Очистить сгенерированные файлы
```

### Команды Git

```bash
# Обновить свою ветку
git fetch upstream
git rebase upstream/main

# Squash коммиты
git rebase -i HEAD~3

# Отменить последний коммит
git reset --soft HEAD~1

# Посмотреть diff
git diff main..feature-branch
```

### Команды pytest

```bash
# Verbose вывод
pytest -v

# Остановить на первой ошибке
pytest -x

# Запустить конкретный тест
pytest tests/test_calculator.py::test_simple_root

# С маркерами
pytest -m slow
```

## Вопросы и поддержка

### Где получить помощь

- **Issues**: Для вопросов о коде и проблем
- **Discussions**: Для общих вопросов и идей
- **Email**: Для приватных вопросов

### Ресурсы

- [Документация Python](https://docs.python.org/3/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [pytest Documentation](https://docs.pytest.org/)
- [Git Documentation](https://git-scm.com/doc)

## Признательность

Спасибо всем, кто вносит вклад в проект! Ваша работа ценится.

### Список участников

Все участники автоматически добавляются в [CONTRIBUTORS.md](CONTRIBUTORS.md).

---

**[🔝 Наверх](#руководство-по-внесению-вклада)** | **[English version](CONTRIBUTING.md)**
