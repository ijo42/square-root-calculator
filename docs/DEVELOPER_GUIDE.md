# Developer Guide

This guide provides information for developers who want to contribute to or extend the Square Root Calculator.

## Development Setup

### Prerequisites
- Python 3.12 or higher
- uv package manager
- Git

### Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/ijo42/square-root-calculator.git
cd square-root-calculator
```

2. Install dependencies:
```bash
uv sync
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Run the application:
```bash
python main.py
```

## Project Architecture

### Directory Structure

```
square-root-calculator/
├── src/square_root_calculator/    # Main application package
│   ├── core/                      # Core calculation logic
│   │   └── calculator.py          # Calculator implementation
│   ├── ui/                        # User interface
│   │   └── main_window.py         # Main GUI window
│   └── locales/                   # Localization
│       └── translator.py          # Translation system
├── docs/                          # Documentation
│   ├── screenshots/               # Application screenshots
│   └── USAGE_EXAMPLES.md          # Usage examples
├── main.py                        # Application entry point
└── pyproject.toml                 # Project configuration
```

### Module Responsibilities

#### `core/calculator.py`
- **SquareRootCalculator**: Main calculator class
  - Manages precision settings
  - Calculates square roots of real numbers
  - Calculates square roots of complex numbers
  - Formats results for display
- **Error Classes**: Custom exceptions for error handling

#### `ui/main_window.py`
- **MainWindow**: Main application window (QMainWindow)
  - Manages UI layout and widgets
  - Handles user interactions
  - Displays results and errors
  - Integrates calculator and translator

#### `locales/translator.py`
- **Translator**: Localization system
  - Stores translations for multiple languages
  - Provides translation lookup
  - Manages language switching

## Key Design Decisions

### 1. Using Python's Decimal Module
We use the `decimal` module instead of floating-point arithmetic because:
- Provides arbitrary precision
- Avoids floating-point rounding errors
- Suitable for financial and scientific calculations
- Configurable precision

### 2. Separate Calculator and UI
The calculator logic is completely independent of the UI:
- Enables easy testing of calculation logic
- Allows alternative UIs (CLI, web, etc.)
- Follows separation of concerns principle

### 3. Built-in Translation System
Rather than using external translation files:
- Simpler for small applications
- No external file dependencies
- Easy to add new languages
- All translations in one place

### 4. PyQt6 for GUI
PyQt6 was chosen because:
- Cross-platform (Windows, Linux)
- Modern, native-looking widgets
- Excellent Python bindings
- Active development and support

## Adding New Features

### Adding a New Language

1. Edit `src/square_root_calculator/locales/translator.py`
2. Add a new language code to the `TRANSLATIONS` dictionary:

```python
TRANSLATIONS = {
    'en': { ... },
    'ru': { ... },
    'fr': {  # New language
        'app_title': 'Calculatrice de Racine Carrée',
        'input_label': 'Valeur d\'entrée:',
        # ... add all translation keys
    }
}
```

3. Update the `get_available_languages` method if needed
4. Test the new language in the UI

### Adding New Calculation Features

To add a new calculation function:

1. Add the calculation method to `SquareRootCalculator`:
```python
def new_calculation(self, value: Union[int, float, str]) -> Decimal:
    """Your new calculation."""
    # Implementation
    pass
```

2. Add UI elements in `MainWindow` if needed
3. Connect UI elements to the calculation method
4. Add translations for any new UI text
5. Test thoroughly

### Extending Precision

To modify precision limits:

1. Edit `main_window.py`:
```python
self.precision_spinbox.setMaximum(2000)  # Increase limit
```

2. Consider performance implications for very high precision

## Testing

### Manual Testing

Run the application and verify:
- Real number calculations
- Complex number calculations
- Precision adjustment
- Language switching
- Error handling

### Automated Testing

Create test files in a `tests/` directory:

```python
# tests/test_calculator.py
from src.square_root_calculator.core.calculator import SquareRootCalculator

def test_real_sqrt():
    calc = SquareRootCalculator()
    result = calc.sqrt_real(16)
    assert result == 4

def test_complex_sqrt():
    calc = SquareRootCalculator()
    real, imag = calc.sqrt_complex(3, 4)
    assert real == 2
    assert imag == 1
```

Run with pytest:
```bash
uv pip install pytest
pytest tests/
```

## Code Style

### Python Style Guide
Follow PEP 8 guidelines:
- 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes

### Type Hints
Use type hints for better code clarity:
```python
def sqrt_real(self, value: Union[int, float, str, Decimal]) -> Decimal:
    """Calculate square root with type hints."""
    pass
```

## Common Development Tasks

### Adding Dependencies

```bash
uv add package-name
```

### Removing Dependencies

```bash
uv remove package-name
```

### Updating Dependencies

```bash
uv sync --upgrade
```

### Building Distribution

```bash
uv build
```

## Debugging

### Enable Debug Output

Add debug prints to trace execution:
```python
import sys
print(f"Debug: {variable}", file=sys.stderr)
```

### Qt Debug Messages

Set environment variable for Qt debugging:
```bash
export QT_DEBUG_PLUGINS=1
python main.py
```

### Using Python Debugger

```python
import pdb; pdb.set_trace()
```

## Performance Considerations

### High Precision Impact
- Precision > 100: Noticeable computation time
- Precision > 500: May take several seconds
- Consider adding progress indicators for long operations

### GUI Responsiveness
- Long calculations should run in separate threads
- Use `QThread` for background processing
- Update UI via signals/slots

## Security Considerations

1. **Input Validation**: Always validate user input
2. **No Eval**: Never use `eval()` on user input
3. **Dependencies**: Keep dependencies up to date
4. **Error Messages**: Don't expose internal details

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

### Commit Message Format
```
<type>: <description>

<detailed explanation if needed>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat: Add cube root calculation

Implements cube root calculation with the same precision
features as square root.
```

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG
3. Create git tag
4. Build distribution
5. Publish to PyPI (if applicable)

## Resources

- [Python Decimal Documentation](https://docs.python.org/3/library/decimal.html)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [PEP 8 Style Guide](https://pep8.org/)

## Getting Help

- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation and examples

## License

This project is open source. Please review the LICENSE file for details.
